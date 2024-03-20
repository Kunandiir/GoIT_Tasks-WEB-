import json
import psycopg2

# Define your PostgreSQL connection details
db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "qwerty123",
    "host": "localhost",
    "port": 5432
}

with open("Task_1/authors.json", "r", encoding="utf-8") as authors_file:
    authors_data = json.load(authors_file)

with open("Task_1/quotes.json", "r", encoding="utf-8") as quotes_file:
    quotes_data = json.load(quotes_file)

conn = psycopg2.connect(**db_params)
cur = conn.cursor()




for author in authors_data:
    cur.execute("""
        INSERT INTO quotes_task_author (full_name, born_date, born_location, description)
        VALUES (%s, %s, %s, %s)
    """, (author["full_name"], author["born_date"], author["born_location"], author["description"]))


for quote in quotes_data:
    # Get the author_id for the quote
    cur.execute("SELECT id FROM quotes_task_author WHERE full_name = %s", (quote["author_name"],))
    result = cur.fetchone()
    if result:
        author_id = result[0]
        print(f"Author ID for {quote['author_name']} is {author_id}")
    else:
        print(f"No author found for {quote['author_name']}")
    cur.execute("SELECT id FROM quotes_task_author WHERE full_name = %s", (quote["author_name"],))
    #author_id = cur.fetchone()[0]
    try:
        author_id = cur.fetchone()[0]
    except TypeError:
        print(f"No author found for {quote['author_name']}")
    cur.execute("""
        INSERT INTO quotes_task_quote (quote_text, tags, author_id)
        VALUES (%s, %s, %s)
    """, (quote["quote_text"], quote['tags'], author_id))

conn.commit()
cur.close()
conn.close()

print("Data imported successfully into PostgreSQL with relations between authors and quotes.")
