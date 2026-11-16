from src.models.board import Board
from src.storage.base import BaseStorage


class DatabaseStorage(BaseStorage):
    def __init__(self, conn_str: str):
        super().__init__()

        self.conn_str = conn_str

    def load_board(id: int) -> Board | None:
        pass

    def save_board(board: Board) -> bool:
        pass