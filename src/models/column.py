from dataclasses import dataclass, field
from uuid import UUID

from .task import Task


@dataclass
class Column:
    id: int
    name: str
    order: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        if any(t.id == task.id for t in self.tasks):
            raise ValueError(f"task {task.id} already exists in column {self.id}")
        
        self.tasks.append(task)

    def remove_task(self, task_id: UUID) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]
