import sqlite3
#Find the average grade given by a specific teacher to a specific student:
def query_11():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT students.name, AVG(marks.value) as average_grade
        FROM marks
        JOIN students ON students.id = marks.student_id_fn
        JOIN subjects ON subjects.id = marks.subject_id_fn
        WHERE marks.student_id_fn = 1 AND subjects.lector_id_fn = 3
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_11())