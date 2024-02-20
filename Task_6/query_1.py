import sqlite3
#Find 5 students with the highest average grade across all subjects:
def query_1():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT students.name, AVG(marks.value) as average_grade
        FROM marks
        JOIN students ON students.id = marks.student_id_fn
        GROUP BY marks.student_id_fn
        ORDER BY average_grade DESC
        LIMIT 5;
        """
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_1())