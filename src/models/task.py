from dataclasses import dataclass
from uuid import UUID

from .user import User


@dataclass
class Task:
    id: UUID
    title: str
    description: str
    order: int
    assignee: User | None = None
