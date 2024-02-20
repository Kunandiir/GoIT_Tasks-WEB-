from table import Table
from dataclasses import dataclass

@dataclass
class Student:
    id: int
    name: str
    group_id_fn: int

class StudentsTable(Table):
    def __init__(self):
        super().__init__(
            "students",
            {
                "id": "integer PRIMARY KEY NOT NULL",
                "name": "varchar(255) NOT NULL",
                "group_id_fn": "integer NOT NULL"
            },
            ["FOREIGN KEY(group_id_fn) REFERENCES groups(id)"]
        )

    def create(self, student: Student) -> int | None:
        return super().create(student.__dict__)

    def get_all(self) -> list[Student] | None:
        result = []
        rows = super().get_all()

        for i in rows:
            result.append(Student(*i))
        
        return result

    def update(self, student: Student, **kwargs):
        super().update(student.__dict__, kwargs)
