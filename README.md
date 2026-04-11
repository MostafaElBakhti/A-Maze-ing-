*This project has been created as part of the 42 curriculum by mostafa.*

# A-Maze-ing

## Description
A-Maze-ing is a Python maze generator that reads a config file, creates a random maze,
adds a centered hardcoded "42" pattern made of fully closed cells, computes a shortest
path from entry to exit, exports the maze in hexadecimal wall format, and shows an ASCII
rendering in terminal.

The project provides:
- A main executable script: `a_maze_ing.py`
- A reusable generation module with one main class: `MazeGenerator` in `maze_generator.py`
- Config and output helpers in `maze_utils.py`
- ASCII visualization in `visualizer.py`

## Instructions

### 1) Install
```bash
make install
```

### 2) Run
```bash
python3 a_maze_ing.py config.txt
```
or
```bash
make run
```

### 3) Debug
```bash
make debug
```

### 4) Lint and type-check
```bash
make lint
```

Optional strict mode:
```bash
make lint-strict
```

### 5) Clean generated caches/build files
```bash
make clean
```

## Configuration File Format
One key-value pair per line with `KEY=VALUE` syntax.
Comments are allowed with `#` at line start.

Mandatory keys:
- `WIDTH`: maze width in cells
- `HEIGHT`: maze height in cells
- `ENTRY`: `x,y`
- `EXIT`: `x,y`
- `OUTPUT_FILE`: output filename
- `PERFECT`: `True` or `False`

Optional keys:
- `SEED`: integer random seed
- `INTERACTIVE`: enable interactive terminal controls
- `SHOW_PATH`: show shortest path in visual output by default

Example:
```txt
WIDTH=21
HEIGHT=21
ENTRY=1,1
EXIT=19,19
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
INTERACTIVE=False
SHOW_PATH=False
```

## Generation Algorithm
The generator uses a simple iterative depth-first search (recursive backtracker style):
- Start from one open cell.
- Randomly visit non-visited neighbors.
- Open walls between current and selected neighbor.
- Backtrack when blocked.

Why this algorithm:
- Easy to understand and explain.
- Produces coherent mazes with valid wall consistency.
- Naturally gives a perfect maze when enabled.

When `PERFECT=False`, generation still works with the same simple core algorithm.

## 42 Pattern Rule
The "42" shape is hardcoded and centered in the maze using fully closed cells.
- Entry and exit are rejected if they fall inside the 42 shape.
- If the maze is too small for the pattern, a warning is shown and generation continues.

## Output File Format
The output file contains:
1. Maze rows in hexadecimal (one hex char per cell)
2. A blank line
3. Entry coordinates line (`x,y`)
4. Exit coordinates line (`x,y`)
5. Shortest path line as directions (`N`, `E`, `S`, `W`)

All lines end with a newline.

## Reusable Code
The reusable component is the `MazeGenerator` class from `maze_generator.py`.

Basic example:
```python
from maze_generator import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    is_perfect=True,
    seed=42,
)
generator.generate()
hex_rows = generator.to_hex_rows()
path_steps = generator.shortest_path()
```

This project includes `pyproject.toml` metadata so it can be built as package
`mazegen-a-maze-ing`.

## Team and Project Management
- Team size: 1 (mostafa)
- Role split:
  - Architecture and algorithm: mostafa
  - Config/output format handling: mostafa
  - Visualization and CLI behavior: mostafa
- Planning:
  - Step 1: read and map subject constraints
  - Step 2: implement generator and serialization
  - Step 3: add parser, visualization, and interactions
  - Step 4: lint/type-check and fix issues
- What worked well:
  - Building around one reusable generator class simplified integration.
- What can be improved:
  - Add more tests and optional additional algorithms.
- Tools used:
  - Python 3.10+
  - flake8
  - mypy
  - Make

## Resources
- Python documentation: https://docs.python.org/3/
- Random module docs: https://docs.python.org/3/library/random.html
- Dataclasses docs: https://docs.python.org/3/library/dataclasses.html
- Graph traversal basics (DFS/BFS)

### AI Usage Disclosure
AI was used for:
- Structuring file/module organization
- Drafting code templates and documentation wording
- Reviewing edge cases and subject-compliance checklist

All generated code was reviewed and adapted before use.
