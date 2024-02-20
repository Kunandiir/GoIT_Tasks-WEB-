import sqlite3
#Find the list of courses attended by a student:
def query_9():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT subjects.name
        FROM marks
        JOIN subjects ON subjects.id = marks.subject_id_fn
        WHERE marks.student_id_fn = 1;
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_9())