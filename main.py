from src.app import Application
from src.storage.json_board import JsonStringBoardRepository


def main():
    app = Application()
    app.create_board(
        "board-1",
        "My Kanban",
        [(1, "To Do"), (2, "In Progress"), (3, "Done")],
    )

    task = app.create_task("board-1", 1, "Write DDD example")
    print("Created task:", task)

    app.move_task("board-1", task["id"], 2)
    print(app.render_board("board-1"))

    json_app = Application(JsonStringBoardRepository())
    json_app.create_board(
        "board-1",
        "My Kanban",
        [(1, "To Do"), (2, "In Progress"), (3, "Done")],
    )
    print("Board from JSON repo:", json_app.render_board("board-1"))


if __name__ == "__main__":
    main()
