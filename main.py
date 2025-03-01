from dotenv import load_dotenv
from openai import OpenAI
import questionary
import questionary.question
from rich.syntax import Syntax
from rich.console import Console
import sqlite3

def get_database(db_path: str) -> tuple:
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS perishables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity FLOAT NOT NULL,
    unit TEXT NOT NULL,
    location TEXT NOT NULL,
    purchase_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status TEXT CHECK (status IN ('Fresh', 'Expired', 'Consumed', 'Discarded')) NOT NULL,
    notes TEXT NULL
);
    """)
    db.commit()
    return db, cursor

def generate_chat_completion(client: OpenAI, prompt: str, system_prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

def get_unique_values(cursor: sqlite3.Cursor, column: str) -> list:
    cursor.execute("SELECT DISTINCT ? FROM perishables;", (column,))
    return [row[0] for row in cursor.fetchall()]

if __name__ == "__main__":
    with open("system-prompt.md", "r") as file:
        system_prompt = file.read()

    prompt = questionary.text("What would you like to do?", multiline=True).ask()
    if not prompt:
        exit()

    db, cursor = get_database("perishables.db")
    load_dotenv()
    client = OpenAI()
    console = Console()

    system_prompt += f"\n\nCurrent perishables in the database: {",".join(get_unique_values(cursor, 'name'))}"
    system_prompt += f"\nCurrent categories in the database: {','.join(get_unique_values(cursor, 'category'))}"

    sql_command = generate_chat_completion(client, prompt, system_prompt)
    syntax = Syntax(sql_command, "sql", theme="monokai", line_numbers=True, word_wrap=True)
    console.print(syntax)
    
    if questionary.confirm("Would you like to execute the SQL command?").ask():
        cursor.execute(sql_command)
        db.commit()