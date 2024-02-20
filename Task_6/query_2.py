import sqlite3
#Find the student with the highest average grade in a specific subject:
#display name
def query_2():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT students.name, AVG(marks.value) as average_grade
        FROM marks
        JOIN students ON students.id = marks.student_id_fn
        WHERE marks.subject_id_fn = 3
        GROUP BY marks.student_id_fn
        ORDER BY average_grade DESC
        LIMIT 1;
        """
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_2())