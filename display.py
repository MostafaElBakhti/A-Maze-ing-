import sys
import os


def print_maze(mg, grid, path=None, show_path=False,
               wall_color="\033[94m"):
    COLOR_WALL = wall_color
    COLOR_SOLUTION = "\033[96m"
    COLOR_RESET = "\033[0m"

    TOP_LEFT = "╔"
    TOP_RIGHT = "╗"
    H_LINE = "═"
    V_LINE = "║"
    CROSS = "╬"
    T_DOWN = "╦"
    T_RIGHT = "╠"
    T_LEFT = "╣"

    path_coords = set()
    if show_path and path:
        path_coords = set(mg.path_to_coords(path))

    print(COLOR_WALL + TOP_LEFT
          + (H_LINE * 3 + T_DOWN) * (mg.width - 1)
          + H_LINE * 3 + TOP_RIGHT + COLOR_RESET)

    for y in range(mg.height):
        row = COLOR_WALL + V_LINE + COLOR_RESET
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
                row += COLOR_WALL + V_LINE + COLOR_RESET
            else:
                row += " "
        print(row)

        row = COLOR_WALL + T_RIGHT + COLOR_RESET
        for x in range(mg.width):
            cell = grid[y][x]
            if cell.walls["S"]:
                row += COLOR_WALL + H_LINE * 3 + COLOR_RESET
            else:
                row += "   "
            if x < mg.width - 1:
                row += COLOR_WALL + CROSS + COLOR_RESET
            else:
                row += COLOR_WALL + T_LEFT + COLOR_RESET
        print(row)


def interactive_menu(mg, grid, path):
    show_path = False
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
            print("4. Quit")

            choice = input("Choice (1-4): ").strip()

            if choice == "1":
                os.system('clear')
                grid, path = mg.generate()
                show_path = False

            elif choice == "2":
                os.system('clear')
                show_path = not show_path
                status = "shown" if show_path else "hidden"
                print(f"Path {status}")

            elif choice == "3":
                os.system('clear')
                color_index = (color_index + 1) % len(colors)

            elif choice == "4":
                print("Bye!")
                sys.exit(0)

            else:
                print("Invalid choice, please enter 1-4")

        except KeyboardInterrupt:
            print("\nBye!")
            sys.exit(0)