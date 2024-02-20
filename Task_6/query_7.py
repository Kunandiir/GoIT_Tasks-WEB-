import sqlite3
#Find the grades of students in a specific group for a specific subject:
def query_7():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT students.name, marks.value
        FROM marks
        JOIN students ON students.id = marks.student_id_fn
        WHERE marks.subject_id_fn = 4 AND students.group_id_fn = 3;
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_7())