from uuid import UUID, uuid4

from src.models.board import Board
from src.models.task import Task
from src.storage.base import BoardRepository


class KanbanService:
    def __init__(self, repository: BoardRepository):
        self._repository = repository

    def get_board(self, board_id: str) -> Board:
        board = self._repository.find_by_id(board_id)
        if board is None:
            raise ValueError(f"Board {board_id} not found")
        return board

    def create_task(
        self, board_id: str, column_id: int, title: str, description: str = ""
    ) -> Task:
        board = self.get_board(board_id)
        column = next((c for c in board.columns if c.id == column_id), None)
        if column is None:
            raise ValueError(f"Column {column_id} not found")

        task = Task(
            id=uuid4(),
            title=title,
            description=description,
            order=len(column.tasks) + 1,
        )
        column.add_task(task)
        self._repository.save(board)
        return task

    def move_task(
        self, board_id: str, task_id: UUID, new_column_id: int
    ) -> None:
        board = self.get_board(board_id)
        board.move_task(task_id, new_column_id)
        self._repository.save(board)

    def delete_task(self, board_id: str, task_id: UUID) -> None:
        board = self.get_board(board_id)
        board.delete_task(task_id)
        self._repository.save(board)
