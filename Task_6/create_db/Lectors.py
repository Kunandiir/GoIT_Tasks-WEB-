from table import Table
from dataclasses import dataclass

@dataclass
class Lector:
    id: int
    name: str

class LectorsTable(Table):
    def __init__(self):
        super().__init__(
            "lectors",
            {
                "id": "integer PRIMARY KEY NOT NULL",
                "name": "varchar(255) NOT NULL",
            },
            []
        )



    def create(self, lector: Lector) -> int | None:
        return super().create(lector.__dict__)

    def get_all(self) -> list[Lector] | None:
        result = []
        rows = super().get_all()

        for i in rows:
            result.append(Lector(*i))
        
        return result

    def update(self, lector: Lector, **kwargs):
        super().update(lector.__dict__, kwargs)
