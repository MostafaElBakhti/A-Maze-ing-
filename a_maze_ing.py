import random
from collections import deque
import sys
from parse import get_config
from display import interactive_menu
from mazegen import MazeGenerator


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            sys.exit(1)

        try:
            config = get_config(sys.argv[1])
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

        mg = MazeGenerator(
            width=config['WIDTH'],
            height=config['HEIGHT'],
            entry=config['ENTRY'],
            exit_=config['EXIT'],
            perfect=config['PERFECT'],
            output_file=config['OUTPUT_FILE'],
            seed=config['SEED']
        )

        grid, path = mg.generate()

        if grid is None:
            sys.exit(1)

        interactive_menu(mg, grid, path)

    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
