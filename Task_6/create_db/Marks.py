from table import Table
from dataclasses import dataclass

@dataclass
class Mark:
    id: int
    value: int
    timestamp: str
    subject_id_fn: int
    student_id_fn: int

class MarksTable(Table):
    def __init__(self):
        super().__init__(
            "marks",
            {
                "id": "integer PRIMARY KEY NOT NULL",
                "value": "integer NOT NULL",
                "timestamp": "varchar(255) NOT NULL",
                "subject_id_fn": "integer NOT NULL",
                "student_id_fn": "integer NOT NULL"
            },
            [
                "FOREIGN KEY(subject_id_fn) REFERENCES subjects(id)",
                "FOREIGN KEY(student_id_fn) REFERENCES students(id)"
            ]
        )


    def create(self, mark: Mark) -> int | None:
        return super().create(mark.__dict__)

    def get_all(self) -> list[Mark] | None:
        result = []
        rows = super().get_all()

        for i in rows:
            result.append(Mark(*i))
        
        return result

    def update(self, mark: Mark, **kwargs):
        super().update(mark.__dict__, kwargs)
