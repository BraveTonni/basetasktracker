from uuid import UUID, uuid4

from src.bus.base import EventPublisher
from src.bus.null import NullEventPublisher
from src.models.board import Board
from src.models.task import Task
from src.storage.base import BoardRepository


class KanbanService:
    def __init__(
        self,
        repository: BoardRepository,
        events: EventPublisher | None = None,
    ):
        self._repository = repository
        self._events = events or NullEventPublisher()

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
        self._events.publish(
            "kanban.task.created",
            {
                "board_id": board_id,
                "column_id": column_id,
                "task_id": str(task.id),
                "title": title,
                "description": description,
            },
            event_id=f"task.created:{task.id}",
        )
        return task

    def move_task(
        self, board_id: str, task_id: UUID, new_column_id: int
    ) -> None:
        board = self.get_board(board_id)
        source = next(
            (
                c.id
                for c in board.columns
                if any(t.id == task_id for t in c.tasks)
            ),
            None,
        )
        board.move_task(task_id, new_column_id)
        self._repository.save(board)
        self._events.publish(
            "kanban.task.moved",
            {
                "board_id": board_id,
                "task_id": str(task_id),
                "from_column_id": source,
                "to_column_id": new_column_id,
            },
        )

    def delete_task(self, board_id: str, task_id: UUID) -> None:
        # TODO: make permission for task delete (to owner/admin)...
        board = self.get_board(board_id)
        board.delete_task(task_id)
        self._repository.save(board)
        self._events.publish(
            "kanban.task.deleted",
            {
                "board_id": board_id,
                "task_id": str(task_id),
            },
            event_id=f"task.deleted:{task_id}",
        )
