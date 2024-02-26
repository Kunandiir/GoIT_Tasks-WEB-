from faker import Faker
from sqlalchemy import create_engine, DateTime, String, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from sqlalchemy.orm import Mapped, mapped_column, relationship

engine = create_engine('postgresql://postgres:qwerty123@localhost:6543/postgres')

DBSession = sessionmaker(bind=engine) # Abstract sessions factory

def fake_date_time():
    return Faker().date_time()

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    marks: Mapped[list["Mark"]] = relationship('Mark', backref='student')

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    students: Mapped[list["Student"]] = relationship('Student', backref='group')

class Mark(Base):
    __tablename__ = 'marks'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()
    timestamp: Mapped[DateTime] = mapped_column(DateTime)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))

class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    lector_id: Mapped[int] = mapped_column(ForeignKey('lectors.id'))
    marks: Mapped[list["Mark"]] = relationship('Mark', backref='subject')

class Lector(Base):
    __tablename__ = 'lectors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    subjects: Mapped[list["Subject"]] = relationship('Subject', backref='lector')


def init_db():
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


#def show_db():



def drop_db():
    with DBSession() as session:
        session.query(Mark).delete()
        session.query(Student).delete()
        session.query(Group).delete()
        session.query(Subject).delete()
        session.query(Lector).delete()
  
        session.commit()

def reset_db():
    Base.metadata.drop_all(engine)



if __name__ == "__main__":
    reset_db()
    init_db()
    #drop_db()



