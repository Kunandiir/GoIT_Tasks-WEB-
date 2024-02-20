import sqlite3
#Find the list of students in a specific group:
def query_6():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT name
        FROM students
        WHERE group_id_fn = 3;
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_6())