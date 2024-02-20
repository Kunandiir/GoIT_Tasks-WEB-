import sqlite3
#Find the average grade in groups for a specific subject:
def query_3():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT groups.name, AVG(marks.value) as average_grade
        FROM marks
        JOIN students ON students.id = marks.student_id_fn
        JOIN groups ON students.group_id_fn = groups.id
        WHERE marks.subject_id_fn = 1
        GROUP BY groups.name;

        """
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_3())