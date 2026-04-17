*This project has been created as part of the 42 curriculum by mel-bakh, zhamza.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator that:

- reads a configuration file,
- generates a random maze with optional deterministic seed,
- writes the maze to a hexadecimal wall-encoded output file,
- computes and stores a shortest valid path from entry to exit,
- provides an interactive terminal visualization.

The project also includes a reusable generator module in the `mazegen` package.

## Features

- DFS-based random maze carving.
- Optional perfect maze mode (`PERFECT=True`).
- Optional non-perfect mode by opening extra random walls (`PERFECT=False`).
- Validation and parsing for mandatory config keys.
- Hexadecimal output format (N/E/S/W encoded as bits 0/1/2/3).
- Shortest path computation using BFS.
- "42" pattern insertion using locked/closed cells (skipped with warning if maze too small).
- 3x3 open-area detection and correction.
- Interactive terminal rendering with:
	- maze regeneration,
	- show/hide shortest path,
	- wall color cycling.

## Project Structure

- `a_maze_ing.py`: main entry point, `MazeGenerator` class used by the app.
- `parse.py`: configuration parsing and validation.
- `display.py`: terminal rendering and interaction menu.
- `config.txt`: default configuration file.
- `maze.txt`: generated output file.
- `mazegen/mazegen.py`: reusable maze-generation module.
- `Makefile`: install/run/debug/clean/lint targets.

## Instructions

### Requirements

- Python 3.10+ (project `pyproject.toml` currently targets Python 3.12).
- `flake8`, `mypy`, `build` for lint/build workflows.

### Install Dependencies

```bash
make install
```

### Run

```bash
python3 a_maze_ing.py config.txt
```

or

```bash
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

Optional strict mode:

```bash
make lint-strict
```

### Clean Build/Cache Artifacts

```bash
make clean
```

### Build Python Package

```bash
python3 -m build
```

## Usage

```bash
python3 a_maze_ing.py config.txt
```

The program reads `config.txt`, generates a maze, writes the encoded file (for example `maze.txt`), then opens an interactive terminal interface.

Interactive menu:

1. Re-generate a new maze.
2. Show/Hide shortest path.
3. Change wall color.
4. Quit.

## Configuration File Format

One `KEY=VALUE` per line.

- Empty lines are ignored.
- Lines starting with `#` are comments.
- Keys are case-insensitive in practice (internally normalized to uppercase).

### Mandatory Keys

| Key | Type | Example | Description |
|---|---|---|---|
| `WIDTH` | int | `WIDTH=20` | Maze width in cells |
| `HEIGHT` | int | `HEIGHT=15` | Maze height in cells |
| `ENTRY` | `x,y` | `ENTRY=0,0` | Entry cell coordinates |
| `EXIT` | `x,y` | `EXIT=19,14` | Exit cell coordinates |
| `OUTPUT_FILE` | string | `OUTPUT_FILE=maze.txt` | Output filename |
| `PERFECT` | bool | `PERFECT=True` | Perfect maze mode |

### Optional Keys

| Key | Type | Example | Description |
|---|---|---|---|
| `SEED` | int/float/string/None | `SEED=42` | Random seed for reproducible generation |

### Default Config In This Repository

```ini
# Default Configuration
width=19
HEIGHT=17
ENTRY=0,0
EXIT=13,10
OUTPUT_FILE=maze.txt
perfect=false
```

## Output File Format

Each maze cell is encoded as one hexadecimal digit.

Bit mapping:

- bit `0` (value `1`): North wall closed
- bit `1` (value `2`): East wall closed
- bit `2` (value `4`): South wall closed
- bit `3` (value `8`): West wall closed

Cells are written row by row, one line per row.

After one empty line:

1. Entry coordinates (`x,y`)
2. Exit coordinates (`x,y`)
3. Shortest path as letters `N`, `E`, `S`, `W` (or `NO_PATH`)

## Algorithm

### Chosen Algorithm

Depth-First Search recursive backtracker (implemented iteratively with a stack) is used to carve the maze.

### Why This Algorithm

- Simple and robust to implement.
- Produces clear corridor-like mazes.
- Works well with random seeds for reproducibility.
- Easy to adapt for perfect/non-perfect variants.

### Additional Steps

- Inject closed-cell "42" pattern when size permits.
- Post-process to prevent 3x3 fully open areas.
- In non-perfect mode, break selected walls randomly.
- Compute shortest path with BFS.

## Reusable Module

Reusable part: `mazegen/mazegen.py` with class `MazeGenerator`.

### Basic Example

```python
from mazegen import MazeGenerator

mg = MazeGenerator(
		width=19,
		height=17,
		entry=(0, 0),
		exit_=(13, 10),
		perfect=True,
		output_file="maze.txt",
		seed=42,
)

grid, path = mg.generate()
print(path)
```

### Custom Parameters

- Size: `width`, `height`
- Reproducibility: `seed`
- Topology mode: `perfect`
- Endpoints: `entry`, `exit_`
- Output destination: `output_file`

### Accessing Generated Data

- `grid`: matrix of `Cell` objects with wall states (`N`, `E`, `S`, `W`).
- `path`: shortest path directions as a list, for example `['E', 'E', 'S']`.
- You can convert path directions to coordinates via `path_to_coords(path)`.

## Team And Project Management

### Team Roles

- `mel-bakh`: everything other than display and parsing.
- `zhamza`: display and parsing.

### Initial Plan

1. Parse and validate config input.
2. Implement generation and output encoder.
3. Add pathfinding.
4. Add terminal UI and interactions.
5. Add lint/build workflow and packaging.

### How It Evolved

- Added constraints handling ("42" pattern and 3x3 area fixes) after core generation worked.
- Stabilized interactive rendering and usability after initial output format validation.
- Packaging/layout work progressed in parallel with feature completion.

### What Worked Well

- Clear separation: parsing, generation, rendering.
- Fast iteration using deterministic seeds.
- Makefile targets helped keep workflows consistent.

### What Could Be Improved

- Increase automated test coverage (unit + integration tests).
- Strengthen typing/docstrings consistency for strict linting.
- Align package naming/versioning fully with subject naming expectations.

### Tools Used

- Python 3
- Make
- flake8
- mypy
- build
- Git

## Subject Coverage Notes

- Main command: `python3 a_maze_ing.py config.txt`.
- Config parsing includes mandatory fields and error handling.
- Output includes encoded maze + entry/exit + shortest path.
- Visual representation is terminal-based with required interactions.
- Reusable generator class exists in `mazegen` package and is documented above.

## Resources

### Maze Generation And Pathfinding

- Jamis Buck, "Maze Generation: Recursive Backtracking": https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
- Wikipedia, "Maze generation algorithm": https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Wikipedia, "Breadth-first search": https://en.wikipedia.org/wiki/Breadth-first_search

### Python Packaging And Quality

- Python Packaging User Guide: https://packaging.python.org/
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- PEP 257 Docstring Conventions: https://peps.python.org/pep-0257/
- mypy documentation: https://mypy.readthedocs.io/
- flake8 documentation: https://flake8.pycqa.org/

### AI Usage Disclosure

AI tools were used for:

- drafting and improving documentation structure,
- refining wording for explanations,
- checking completeness against subject checklist.

AI was not used as a blind copy-paste source; generated content was reviewed and adjusted to match the implemented code and project decisions.
