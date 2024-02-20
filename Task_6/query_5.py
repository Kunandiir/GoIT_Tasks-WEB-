import sqlite3
#Find which courses a specific teacher teaches:
def query_5():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT name
        FROM subjects
        WHERE lector_id_fn = 1;
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_5())