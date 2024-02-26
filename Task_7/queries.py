from sqlalchemy import create_engine, func, desc, cast, DateTime
from sqlalchemy.orm import sessionmaker
from main import Student, Group, Mark, Subject, Lector  # replace 'main' with the name of your db file

engine = create_engine('postgresql://postgres:qwerty123@localhost:6543/postgres')
DBSession = sessionmaker(bind=engine)
session = DBSession()

def query_1():

    # Find the 5 students with the highest average grade across all subjects
    return session.query(Student.name, func.round(func.avg(Mark.value), 2).label('avg_grade'))\
        .join(Mark)\
        .group_by(Student.id)\
        .order_by(desc('avg_grade'))\
        .limit(5)\
        .all()
def query_2(subject_id):
    # Find the student with the highest average grade in a specific subject
    return session.query(Student.name, func.round(func.avg(Mark.value), 2).label('avg_grade'))\
        .join(Mark)\
        .join(Subject)\
        .filter(Subject.id == subject_id)\
        .group_by(Student.id)\
        .order_by(desc('avg_grade'))\
        .first()

def query_3(subject_id):
    # Find the average grade in groups for a specific subject
    return session.query(Group.name, func.round(func.avg(Mark.value), 2).label('avg_grade'))\
        .select_from(Group)\
        .join(Student)\
        .join(Mark)\
        .join(Subject)\
        .filter(Subject.id == subject_id)\
        .group_by(Group.id)\
        .all()

def query_4():
    # Find the average grade across all marks
    return session.query(func.round(func.avg(Mark.value), 2).label('avg_grade'))\
        .first()

def query_5(lector_id):
    # Find the courses taught by a specific lector
    return session.query(Subject.name)\
        .join(Lector)\
        .filter(Lector.id == lector_id)\
        .all()

def query_6(group_id):
    # Find the list of students in a specific group
    return session.query(Student.name)\
        .join(Group)\
        .filter(Group.id == group_id)\
        .all()

def query_7(group_id, subject_id):
    # Find the grades of students in a specific group for a specific subject
    return session.query(Student.name, Mark.value)\
        .join(Group)\
        .join(Mark)\
        .join(Subject)\
        .filter(Group.id == group_id, Subject.id == subject_id)\
        .all()

def query_8(lector_id):
    # Find the average grade given by a specific lector across their subjects
    return session.query(func.round(func.avg(Mark.value), 2).label('avg_grade'))\
        .join(Subject)\
        .join(Lector)\
        .filter(Lector.id == lector_id)\
        .first()

def query_9(student_id):
    # Find the list of courses attended by a specific student
    return session.query(Subject.name)\
        .join(Mark)\
        .join(Student)\
        .filter(Student.id == student_id)\
        .all()

def query_10(student_id, lector_id):
    # Find the list of courses taught by a specific lector to a specific student
    return session.query(Subject.name)\
        .join(Mark)\
        .join(Student)\
        .join(Lector)\
        .filter(Student.id == student_id, Lector.id == lector_id)\
        .all()


def aditional_query_11(student_id, lector_id):
    # Find the average grade given by a specific lector to a specific student
    return session.query(func.round(func.avg(Mark.value), 2).label('avg_grade'))\
        .join(Student)\
        .join(Subject)\
        .join(Lector)\
        .filter(Student.id == student_id, Lector.id == lector_id)\
        .first()

def aditional_query_12(group_id, subject_id):
    # Find the grades of students in a specific group for a specific subject at the last lesson
    return session.query(Student.name, Mark.value)\
        .select_from(Mark)\
        .join(Student)\
        .join(Group)\
        .join(Subject)\
        .filter(Group.id == group_id, Subject.id == subject_id, Mark.timestamp == session.query(func.max(Mark.timestamp)).scalar_subquery())\
        .all()


if __name__ == "__main__":
    print(query_1())
    print(query_2(3))
    print(query_3(5))
    print(query_4())
    print(query_5(2))
    print(query_6(1))
    print(query_7(2,1))
    print(query_8(1))
    print(query_9(33))
    print(query_10(22,1))
    print(aditional_query_11(21,1))
    print(aditional_query_12(1,3))#idk, can't make it work
