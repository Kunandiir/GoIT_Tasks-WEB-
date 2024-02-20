from table import Table
from dataclasses import dataclass

@dataclass
class Subject:
    id: int
    name: str
    lector_id_fn: int

class SubjectsTable(Table):
    def __init__(self):
        super().__init__(
            "subjects",
            {
                "id": "integer PRIMARY KEY NOT NULL",
                "name": "varchar(255) NOT NULL",
                "lector_id_fn": "integer NOT NULL"
            },
            ["FOREIGN KEY(lector_id_fn) REFERENCES lectors(id)"]
        )



    def create(self, subject: Subject) -> int | None:
        return super().create(subject.__dict__)

    def get_all(self) -> list[Subject] | None:
        result = []
        rows = super().get_all()

        for i in rows:
            result.append(Subject(*i))
        
        return result

    def update(self, subject: Subject, **kwargs):
        super().update(subject.__dict__, kwargs)
