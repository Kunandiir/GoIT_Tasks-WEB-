import sqlite3

with sqlite3.connect("test.sqlite") as conn:
    print(conn)
