import sys
import os
import time
from typing import Any, Optional, List


def print_maze(
    mg: Any,
    grid: List[List[Any]],
    path: Optional[List[Any]] = None,
    show_path: bool = False,
    wall_color: str = "\033[94m",
    path_color: str = "\033[96m",
    path_wall_color: Optional[str] = None,
) -> None:
    COLOR_WALL = wall_color
    COLOR_SOLUTION = path_color
    COLOR_PATH_WALL = path_wall_color if path_wall_color else COLOR_SOLUTION
    COLOR_RESET = "\033[0m"

    TOP_LEFT = "╔"
    TOP_RIGHT = "╗"
    BOT_LEFT = "╚"
    BOT_RIGHT = "╝"
    H_LINE = "═"
    V_LINE = "║"
    CROSS = "╬"
    T_DOWN = "╦"
    T_UP = "╩"
    T_RIGHT = "╠"
    T_LEFT = "╣"

    path_coords = set()
    if show_path and path:
        if (
            isinstance(path, list)
            and len(path) > 0
            and isinstance(path[0], tuple)
        ):
            path_coords = set(path)
        else:
            path_coords = set(mg.path_to_coords(path))

    def touches_path(*cells: tuple[int, int]) -> bool:
        return any(cell in path_coords for cell in cells)

    def paint(symbol: str, highlight: bool = False) -> str:
        color = COLOR_PATH_WALL if highlight else COLOR_WALL
        return color + symbol + COLOR_RESET

    top_row = paint(TOP_LEFT, touches_path((0, 0)))
    for x in range(mg.width):
        top_row += paint(H_LINE * 3, touches_path((x, 0)))
        if x < mg.width - 1:
            top_row += paint(T_DOWN, touches_path((x, 0), (x + 1, 0)))
        else:
            top_row += paint(TOP_RIGHT, touches_path((x, 0)))
    print(top_row)

    for y in range(mg.height):
        row = paint(V_LINE, touches_path((0, y)))
        for x in range(mg.width):
            cell = grid[y][x]
            if cell.locked:
                row += "███"
            elif (x, y) == mg.entry:
                row += "\033[92m" + " E " + COLOR_RESET
            elif (x, y) == mg.exit_:
                row += "\033[91m" + " X " + COLOR_RESET
            elif show_path and (x, y) in path_coords:
                row += COLOR_SOLUTION + " ◆ " + COLOR_RESET
            else:
                row += "   "

            if cell.walls["E"]:
                if x < mg.width - 1:
                    row += paint(V_LINE, touches_path((x, y), (x + 1, y)))
                else:
                    row += paint(V_LINE, touches_path((x, y)))
            else:
                row += " "
        print(row)

        if y == mg.height - 1:
            row = paint(BOT_LEFT, touches_path((0, y)))
            for x in range(mg.width):
                row += paint(H_LINE * 3, touches_path((x, y)))
                if x < mg.width - 1:
                    row += paint(T_UP, touches_path((x, y), (x + 1, y)))
                else:
                    row += paint(BOT_RIGHT, touches_path((x, y)))
            print(row)
        else:
            row = paint(T_RIGHT, touches_path((0, y), (0, y + 1)))
            for x in range(mg.width):
                cell = grid[y][x]
                if cell.walls["S"]:
                    row += paint(H_LINE * 3, touches_path((x, y), (x, y + 1)))
                else:
                    row += "   "
                if x < mg.width - 1:
                    row += paint(
                        CROSS,
                        touches_path(
                            (x, y),
                            (x + 1, y),
                            (x, y + 1),
                            (x + 1, y + 1),
                        ),
                    )
                else:
                    row += paint(T_LEFT, touches_path((x, y), (x, y + 1)))
            print(row)


def animate_path(
    mg: Any,
    grid: List[List[Any]],
    path: List[Any],
    wall_color: str,
    path_wall_color: str = "\033[97m",
    delay: float = 0.3,
) -> None:
    coords = mg.path_to_coords(path)

    for i in range(1, len(coords) + 1):
        os.system("clear")
        partial_path = coords[:i]

        print_maze(
            mg,
            grid,
            path=partial_path,
            show_path=True,
            wall_color=wall_color,
            path_wall_color=path_wall_color,
        )

        time.sleep(delay)


def interactive_menu(
    mg: Any,
    grid: List[List[Any]],
    path: Any,
) -> None:
    show_path = False
    animation_path_wall_color = "\033[97m"
    colors = [
        "\033[94m",
        "\033[91m",
        "\033[93m",
        "\033[92m",
        "\033[95m",
    ]
    color_index = 0

    while True:
        try:
            os.system('clear')
            print_maze(
                mg,
                grid,
                path=path,
                show_path=show_path,
                wall_color=colors[color_index]
            )

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Change wall colour")
            print("4. Animate path")
            print("5. Quit")

            choice = input("Choice (1-5): ").strip()

            if choice == "1":
                grid, path = mg.generate()
                show_path = False

            elif choice == "2":
                show_path = not show_path

            elif choice == "3":
                color_index = (color_index + 1) % len(colors)

            elif choice == "4":
                animate_path(
                    mg,
                    grid,
                    path,
                    wall_color=colors[color_index],
                    path_wall_color=animation_path_wall_color,
                )
                input("Press Enter to continue...")

            elif choice == "5":
                print("Bye!")
                sys.exit(0)

            else:
                print("Invalid choice, please enter 1-5")
                input("Press Enter to continue...")

        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            sys.exit(0)
