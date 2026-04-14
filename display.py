# display.py
import sys
import time
import os


def clear_screen():
    os.system('clear')


def pacman_animation(mg, grid, path):
    """Animate a pacman face eating the path dots."""

    if not path:
        print("No path to animate!")
        return

    path_coords = mg.path_to_coords(path)

    COLOR_WALL = "\033[94m"
    COLOR_DOT = "\033[92m"
    COLOR_RESET = "\033[0m"
    COLOR_EATEN = "\033[90m"   # grey — eaten dots
    COLOR_PACMAN = "\033[93m"  # yellow pacman

    TOP_LEFT = "╔"
    TOP_RIGHT = "╗"
    H_LINE = "═"
    V_LINE = "║"
    CROSS = "╬"
    T_DOWN = "╦"
    T_RIGHT = "╠"
    T_LEFT = "╣"

    # pacman frames — mouth opening and closing
    PACMAN_FRAMES = ["ᗧ", "●"]

    frame = 0
    eaten = set()

    for i, (px, py) in enumerate(path_coords):
        clear_screen()

        eaten.add((px, py))

        # top border
        print(COLOR_WALL + TOP_LEFT
              + (H_LINE * 3 + T_DOWN) * (mg.width - 1)
              + H_LINE * 3 + TOP_RIGHT + COLOR_RESET)

        for y in range(mg.height):
            row = COLOR_WALL + V_LINE + COLOR_RESET
            for x in range(mg.width):
                cell = grid[y][x]

                if cell.locked:
                    row += "███"
                elif (x, y) == (px, py):
                    # current pacman position
                    row += COLOR_PACMAN + f" {PACMAN_FRAMES[frame]} " + COLOR_RESET
                elif (x, y) in eaten:
                    # eaten dots — show empty
                    row += COLOR_EATEN + " · " + COLOR_RESET
                elif (x, y) in set(path_coords):
                    # uneaten dots
                    row += COLOR_DOT + " • " + COLOR_RESET
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

        steps_left = len(path_coords) - i - 1
        print(f"\n{COLOR_PACMAN}ᗧ•••{COLOR_RESET} Step {i + 1}/{len(path_coords)} "
              f"— {steps_left} dots left")

        frame = (frame + 1) % 2
        time.sleep(0.15)

    # final frame — pacman reached exit
    clear_screen()
    print_maze(mg, grid, path=path, show_path=False)
    print(f"\n{COLOR_PACMAN}ᗧ  Pacman reached the exit! "
          f"Path length: {len(path)} steps{COLOR_RESET}")


def print_maze(mg, grid, path=None, show_path=False,
               wall_color="\033[94m"):
    COLOR_WALL = wall_color
    COLOR_PATH = "\033[92m"
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
            elif show_path and (x, y) in path_coords:
                row += COLOR_SOLUTION + " ◆ " + COLOR_RESET
            else:
                row += COLOR_PATH + " • " + COLOR_RESET

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
        "\033[94m",   # blue
        "\033[91m",   # red
        "\033[93m",   # yellow
        "\033[92m",   # green
        "\033[95m",   # magenta
    ]
    color_index = 0

    while True:
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
            grid, path = mg.generate()
            show_path = False

        elif choice == "2":
            show_path = not show_path
            status = "shown" if show_path else "hidden"
            print(f"Path {status}")

        elif choice == "3":
            color_index = (color_index + 1) % len(colors)

        elif choice == "4":
            print("Bye!")
            sys.exit(0)

        else:
            print("Invalid choice, please enter 1-4")