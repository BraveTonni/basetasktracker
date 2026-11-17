from src.bus.base import EventPublisher
from src.core.controller import KanbanController
from src.core.kanban import KanbanService
from src.models.board import Board
from src.models.column import Column
from src.storage.base import BoardRepository
from src.storage.in_memory import InMemoryBoardRepository


class Application:
    def __init__(
        self,
        repository: BoardRepository | None = None,
        events: EventPublisher | None = None,
    ):
        if repository is None:
            repository = InMemoryBoardRepository()

        self._repository = repository
        self._service = KanbanService(repository, events)
        self._controller = KanbanController(self._service)

    def create_board(
        self, board_id: str, name: str, columns: list[tuple[int, str]]
    ) -> None:
        board = Board(board_id, name)

        for column_id, column_name in columns:
            board.add_column(Column(column_id, column_name, column_id))

        self._repository.save(board)

    def create_task(self, board_id: str, column_id: int, title: str) -> dict:
        return self._controller.create_task(board_id, column_id, title)

    def move_task(
        self, board_id: str, task_id: str, new_column_id: int
    ) -> dict:
        return self._controller.move_task(board_id, task_id, new_column_id)

    def get_board(self, board_id: str) -> dict:
        return self._controller.get_board(board_id)

    def render_board(self, board_id: str) -> str:
        board = self._controller.get_board(board_id)
        lines = [board["name"]]

        for column in board["columns"]:
            lines.append(f"[{column['id']}] {column['name']}")

            for task in column["tasks"]:
                lines.append(f"  - {task['title']} ({task['id']})")

        return "\n".join(lines)
