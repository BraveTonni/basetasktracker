from abc import ABC, abstractmethod

from src.models.board import Board


class BoardRepository(ABC):
    @abstractmethod
    def find_by_id(self, board_id: str) -> Board | None:
        ...

    @abstractmethod
    def save(self, board: Board) -> None:
        ...
