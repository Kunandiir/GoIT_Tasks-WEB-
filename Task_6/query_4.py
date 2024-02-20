import sqlite3
#Find the average grade in the stream (across the entire grades table):
def query_4():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        query = """
        SELECT AVG(value) as average_grade
        FROM marks;
        """ 
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    print(query_4())