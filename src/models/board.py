from dataclasses import dataclass

from .column import Column


@dataclass
class Board:
    name: str
    columns: list[Column]