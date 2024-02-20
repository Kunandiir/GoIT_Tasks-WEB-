from table import Table
from dataclasses import dataclass

@dataclass
class Group:
    id: int
    name: str

class GroupsTable(Table):
    def __init__(self):
        super().__init__(
            "groups",
            {
                "id": "integer PRIMARY KEY NOT NULL",
                "name": "varchar(255) NOT NULL",
            },
            []
        )

    def create(self, group: Group) -> int | None:
        return super().create(group.__dict__)

    def get_all(self) -> list[Group] | None:
        result = []
        rows = super().get_all()

        for i in rows:
            result.append(Group(*i))
        
        return result

    def update(self, group: Group, **kwargs):
        super().update(group.__dict__, kwargs)
