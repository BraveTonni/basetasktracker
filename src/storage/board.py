from abc import ABC, abstractmethod

from src.models.board import Board


class BoardStorage(ABC):
    @abstractmethod
    def load_board(id: int) -> Board | None:
        pass

    @abstractmethod
    def save_board(board: Board) -> bool:
        pass