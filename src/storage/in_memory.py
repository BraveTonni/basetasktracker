from src.models.board import Board
from src.storage.base import BoardRepository


class InMemoryBoardRepository(BoardRepository):
    def __init__(self):
        self._storage: dict[str, Board] = {}

    def find_by_id(self, board_id: str) -> Board | None:
        return self._storage.get(board_id)

    def save(self, board: Board) -> None:
        self._storage[board.id] = board
