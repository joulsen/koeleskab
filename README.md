# Koeleskab ❄
An app to track perishable food or items insde your fridge, freezer, pantry etc. 
Implements an LLM agent which adds, removes and updates an SQL database.

# Example use
```
$ python main.py
? What would you like to do?  (Finish with 'Alt+Enter' or 'Esc then Enter')
> I have the following in my bread basket:
  4 flatbread expiring 25 04 25
  6 tortillas expiring 09 06 25
  20 rice paper sheets expering 13 02 26
  2 slices of white bread that probably expire in two days
  1 INSERT INTO perishables (name, category, quantity, unit, location, purchase_date, expiry_date, status) VALUES 
  2 ('Flatbread', 'Grains', 4, 'pieces', 'Bread Basket', CURRENT_DATE, '2025-04-25', 'Fresh'),
  3 ('Tortillas', 'Grains', 6, 'pieces', 'Bread Basket', CURRENT_DATE, '2025-06-09', 'Fresh'),
  4 ('Rice Paper Sheets', 'Grains', 20, 'pieces', 'Bread Basket', CURRENT_DATE, '2026-02-13', 'Fresh'),
  5 ('White Bread', 'Grains', 2, 'pieces', 'Bread Basket', CURRENT_DATE, DATE(CURRENT_DATE, '+2 days'), 'Fresh');
? Would you like to edit the SQL command? No
? Would you like to execute the SQL command? Yes
```

# Setup
Create a file `.env` with the following and insert a valid OpenAI API key.
```toml
OPENAI_API_KEY="****"
```

Then, clone this repo, create a virtual environment, install `requirements.txt` and you are off 🚀