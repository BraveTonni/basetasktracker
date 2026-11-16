from dataclasses import dataclass


@dataclass
class Column:
    name: str
    order: int