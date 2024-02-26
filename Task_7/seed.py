from faker import Faker
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from main import Student, Group, Mark, Subject, Lector, engine  

fake = Faker()

DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_groups(num_groups=3):
    for _ in range(num_groups):
        group = Group(name=fake.word())
        session.add(group)
    session.commit()

def create_students(num_students=40, num_marks_per_student=20):
    for _ in range(num_students):
        # Get a random group
        group = session.query(Group).order_by(func.random()).first()

        if group is not None:  # Ensure a group was found
            student = Student(name=fake.name(), group_id=group.id)
            session.add(student)
            session.flush()  # Ensure the student is assigned an ID

            # Create marks for the student
            for _ in range(num_marks_per_student):
                # Get a random subject
                subject = session.query(Subject).order_by(func.random()).first()
                if subject is not None:  # Ensure a subject was found
                    mark = Mark(value=fake.random_int(min=1, max=100), timestamp=fake.date_time(), student_id=student.id, subject_id=subject.id)
                    session.add(mark)
    session.commit()


def create_marks(num_marks=20):
    for _ in range(num_marks):
        # Get a random student and subject
        student = session.query(Student).order_by(func.random()).first()
        subject = session.query(Subject).order_by(func.random()).first()
        if student is not None and subject is not None:  # Ensure a student and subject were found
            mark = Mark(value=fake.random_int(min=1, max=100), timestamp=fake.date_time(), student_id=student.id, subject_id=subject.id)
            session.add(mark)
    session.commit()

def create_subjects(num_subjects=7):
    for _ in range(num_subjects):
        # Get a random lector
        lector = session.query(Lector).order_by(func.random()).first()
        if lector is not None:  # Ensure a lector was found
            subject = Subject(name=fake.word(), lector_id=lector.id)
            session.add(subject)
    session.commit()

def create_lectors(num_lectors=4):
    for _ in range(num_lectors):
        lector = Lector(name=fake.name())
        session.add(lector)
    session.commit()


if __name__ == "__main__":
    create_groups()
    create_lectors()
    create_subjects()
    create_students()
    #create_marks()
