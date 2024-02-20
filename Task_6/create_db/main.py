import sqlite3
from table import Table
from faker import Faker
from Students import Student, StudentsTable
from Groups import Group, GroupsTable
from Subjects import Subject, SubjectsTable
from Marks import Mark, MarksTable
from Lectors import Lector, LectorsTable

fake = Faker()


def generate_fake_students(student_table, amount):
    for i in range(amount):
        student = Student(
            id=i,
            name=fake.name(),
            group_id_fn=fake.random_int(min=0, max=3)
        )
        student_table.create(student)


def generate_fake_groups(group_table, amount):
    for i in range(amount + 1):
        group = Group(
            id=i,
            name=fake.word()
        )
        group_table.create(group)

def generate_fake_marks(marks_table, amount, student_amount, subject_amount):



    for i in range(amount):
        mark = Mark(
            id=i,
            value=fake.random_int(min=1, max=100),
            timestamp=str(fake.date_time_this_year()),
            subject_id_fn=fake.random_int(min=1, max=subject_amount),
            student_id_fn=fake.random_int(min=1, max=student_amount)
        )
        marks_table.create(mark)


def generate_fake_subjects(subject_table, amount, lector_amount):
    for i in range(amount):
        subject = Subject(
            id=i,
            name=fake.word(),
            lector_id_fn=fake.random_int(min=0, max=lector_amount)
        )
        subject_table.create(subject)

def generate_fake_lectors(lector_table, amount):
    for i in range(amount):
        lector = Lector(
            id=i,
            name=fake.name()
        )
        lector_table.create(lector)


def main():
    with sqlite3.connect("Task_6/test.sqlite") as conn:
        Table.conn = conn
        students_table = StudentsTable()
        groups_table = GroupsTable()
        subjects_table = SubjectsTable()
        marks_table = MarksTable()
        lectors_table = LectorsTable()


        
        students_amount= 40
        groups_amount= 3
        subjects_amount = 7
        lectors_amount = 4

        marks_amount = 400

        generate_fake_students(students_table, students_amount)
        generate_fake_groups(groups_table, groups_amount)
        generate_fake_subjects(subjects_table, subjects_amount, lectors_amount)
        generate_fake_lectors(lectors_table, lectors_amount)
        generate_fake_marks(marks_table, marks_amount, students_amount, subjects_amount)


if __name__ == "__main__":
    main()
