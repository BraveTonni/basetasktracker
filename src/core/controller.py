from uuid import UUID

from src.core.kanban import KanbanService


class KanbanController:
    def __init__(self, service: KanbanService):
        self._service = service

    def get_board(self, board_id: str) -> dict:
        board = self._service.get_board(board_id)
        return {
            "id": board.id,
            "name": board.name,
            "columns": [
                {
                    "id": c.id,
                    "name": c.name,
                    "tasks": [
                        {"id": str(t.id), "title": t.title} for t in c.tasks
                    ],
                }
                for c in board.columns
            ],
        }

    def create_task(
        self, board_id: str, column_id: int, title: str
    ) -> dict:
        task = self._service.create_task(board_id, column_id, title)
        return {"id": str(task.id), "title": task.title}

    def move_task(
        self, board_id: str, task_id: str, new_column_id: int
    ) -> dict:
        self._service.move_task(board_id, UUID(task_id), new_column_id)
        return {"status": "ok"}
