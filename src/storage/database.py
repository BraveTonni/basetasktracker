from src.models.board import Board
from src.storage.base import BoardRepository


class DatabaseStorage(BoardRepository):
    def __init__(self, conn_str: str):
        super().__init__()

        self.conn_str = conn_str

    def find_by_id(self, board_id: str) -> Board | None:
        pass

    def save(self, board: Board) -> None:
        pass
