*This project has been created as part of the 42 curriculum by mel-bakh, zhamza.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It reads a configuration file, generates a random maze (optionally perfect) containing a visible "42" pattern, writes the result to a file using a hexadecimal wall encoding, and displays the maze in the terminal with an interactive menu.

## Instructions

Requirements: Python 3.10 or later, pip.

Install dependencies:
```bash
make install
```

Run the program:
```bash
make run
```

Or directly:
```bash
python3 a_maze_ing.py config.txt
```

Clean build artifacts:
```bash
make clean
```

Run linters:
```bash
make lint
```

## Configuration file format

The config file uses `KEY=VALUE` format, one pair per line. Lines starting with `#` are comments and ignored.

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates x,y | `ENTRY=0,0` |
| `EXIT` | Exit coordinates x,y | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze flag | `PERFECT=True` |
| `SEED` | Random seed (optional) | `SEED=42` |

Example:
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Algorithm

We used the **recursive backtracker** (iterative DFS with a stack) to carve the maze, and **BFS** to find the shortest path between entry and exit.

### Why this algorithm

- Simple to implement and reason about
- Naturally produces a perfect maze — a spanning tree with exactly one path between any two cells
- Easy to extend for imperfect mazes by breaking extra walls after carving
- BFS guarantees the shortest path in an unweighted grid

## Reusable module

The maze generation logic lives in the `mazegen` package, which can be installed and imported in any Python project.

### Build the package

```bash
python -m build
```

This produces `mazegen-0.1.0.tar.gz` and `mazegen-0.1.0-py3-none-any.whl` in `dist/`.

### Install the package

```bash
pip install mazegen-0.1.0.tar.gz
```

### Basic usage

```python
from mazegen import MazeGenerator

mg = MazeGenerator(
    width=13,
    height=9,
    entry=(0, 0),
    exit_=(12, 8),
    perfect=True,
    output_file="maze.txt",
    seed=42
)

grid, path = mg.generate()

print(f"Path length: {len(path)} steps")
print(f"Path: {''.join(path)}")
```

### What's reusable

- `MazeGenerator` class — full maze generation pipeline
- `mg.generate()` — returns `(grid, path)` where `grid` is the 2D cell structure and `path` is a list of directions (`N`, `E`, `S`, `W`) from entry to exit
- Access to walls, locked cells (42 pattern), and the BFS solver are all exposed through the instance

## Resources

Classic references used:
- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker — Jamis Buck's blog](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [BFS shortest path — GeeksforGeeks](https://www.geeksforgeeks.org/shortest-path-unweighted-graph/)
- Python packaging user guide — [packaging.python.org](https://packaging.python.org/)

### AI usage

AI was used as an assistant for:
- Debugging wall encoding and neighbor relations
- Structuring the `MazeGenerator` class and pipeline ordering
- Reviewing config parser edge cases
- Suggesting the `pyproject.toml` layout for the reusable package

All generated ideas were reviewed, tested, and rewritten in our own style before being integrated.

## Team and project management

### Roles
- **mel-bakh** — maze generation (DFS recursive backtracker), BFS shortest path, 42 pattern placement, output file writing, `mazegen` package
- **zhamza** — config file parser (`parse.py`), terminal display and interactive menu (`display.py`)

### Planning

We started by splitting the project into two halves — generation logic vs. user interface and parsing — so we could work in parallel. Initial plan was one week, final integration took about three days extra for validation, error handling, and packaging.

### What worked well
- Clear separation between generation (`mazegen`) and presentation (`display`, `parse`)
- Early agreement on data structures (`Cell` class, wall dictionary)
- Testing each module in isolation before integration

### What could be improved
- More automated unit tests earlier
- Earlier attention to flake8 and mypy compliance

### Tools used
- VS Code
- Python `venv` for virtual environments
- `poetry-core` + `build` for package building
- `flake8` and `mypy` for linting
- Git and GitHub for version control