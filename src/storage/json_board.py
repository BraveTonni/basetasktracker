import json
from uuid import UUID

from src.models.board import Board
from src.models.column import Column
from src.models.task import Task
from src.models.user import User
from src.storage.base import BoardRepository


class JsonStringBoardRepository(BoardRepository):
    def __init__(self):
        self._raw_data: dict[str, str] = {}
        self._cache: dict[str, Board] = {}

    def find_by_id(self, board_id: str) -> Board | None:
        if board_id in self._cache:
            return self._cache[board_id]

        raw = self._raw_data.get(board_id)
        if not raw:
            return None

        data = json.loads(raw)
        board = Board(data["id"], data["name"])
        for col_data in data["columns"]:
            column = Column(
                col_data["id"], col_data["name"], col_data["order"]
            )
            for t in col_data["tasks"]:
                assignee_data = t.get("assignee")
                assignee = User(**assignee_data) if assignee_data else None
                column.tasks.append(
                    Task(
                        id=UUID(t["id"]),
                        title=t["title"],
                        description=t["description"],
                        order=t["order"],
                        assignee=assignee,
                    )
                )
            board._columns.append(column)

        self._cache[board_id] = board
        return board

    def save(self, board: Board) -> None:
        serialized = {
            "id": board.id,
            "name": board.name,
            "columns": [
                {
                    "id": c.id,
                    "name": c.name,
                    "order": c.order,
                    "tasks": [
                        {
                            "id": str(t.id),
                            "title": t.title,
                            "description": t.description,
                            "order": t.order,
                            "assignee": (
                                vars(t.assignee) if t.assignee else None
                            ),
                        }
                        for t in c.tasks
                    ],
                }
                for c in board.columns
            ],
        }
        self._raw_data[board.id] = json.dumps(serialized)
        self._cache[board.id] = board
