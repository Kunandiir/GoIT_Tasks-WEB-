import sqlite3
#Find the grades of students in a specific group for a specific subject in the last class:
def query_12():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT students.name, marks.value
        FROM marks
        JOIN students ON students.id = marks.student_id_fn
        WHERE marks.subject_id_fn = 3 AND students.group_id_fn = 2
        ORDER BY marks.timestamp DESC
        LIMIT (SELECT COUNT(*) FROM students WHERE group_id_fn = 2)
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_12())