from uuid import UUID

from .column import Column


class Board:
    def __init__(self, board_id: str, name: str):
        self.id = board_id
        self.name = name
        self._columns: list[Column] = []

    @property
    def columns(self) -> list[Column]:
        return list(self._columns)

    def add_column(self, column: Column) -> None:
        if any(c.id == column.id for c in self._columns):
            raise ValueError(f"Column {column.id} already exists")
        self._columns.append(column)

    def move_task(self, task_id: UUID, new_column_id: int) -> None:
        source = next(
            (
                c
                for c in self._columns
                if any(t.id == task_id for t in c.tasks)
            ),
            None,
        )
        if source is None:
            raise ValueError(f"Task {task_id} not found on board {self.id}")

        target = next(
            (c for c in self._columns if c.id == new_column_id), None
        )
        if target is None:
            raise ValueError(
                f"Column {new_column_id} not found on board {self.id}"
            )

        task = next(t for t in source.tasks if t.id == task_id)
        source.remove_task(task_id)
        target.add_task(task)

    def delete_task(self, task_id: UUID) -> None:
        for column in self._columns:
            column.remove_task(task_id)
