from src.core.controller import KanbanController
from src.core.kanban import KanbanService
from src.models.board import Board
from src.models.column import Column
from src.storage.base import BoardRepository
from src.storage.in_memory import InMemoryBoardRepository
from src.storage.json_board import JsonStringBoardRepository


def main():
    repository: BoardRepository = InMemoryBoardRepository()
    service = KanbanService(repository)
    controller = KanbanController(service)

    board = Board("board-1", "My Kanban")
    board.add_column(Column(1, "To Do", 1))
    board.add_column(Column(2, "In Progress", 2))
    board.add_column(Column(3, "Done", 3))
    repository.save(board)

    task = controller.create_task("board-1", 1, "Write DDD example")
    print("Created task:", task)

    controller.move_task("board-1", task["id"], 2)
    print("Board state:", controller.get_board("board-1"))

    repo2: BoardRepository = JsonStringBoardRepository()
    repo2.save(board)
    service2 = KanbanService(repo2)
    print("Board from JSON repo:", service2.get_board("board-1").name)


if __name__ == "__main__":
    main()
