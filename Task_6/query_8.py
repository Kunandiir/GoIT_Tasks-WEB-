import sqlite3
#Find the average grade given by a specific teacher across their subjects:
def query_8():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT AVG(marks.value) as average_grade
        FROM marks
        JOIN subjects ON subjects.id = marks.subject_id_fn
        WHERE subjects.lector_id_fn = 3;
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_8())