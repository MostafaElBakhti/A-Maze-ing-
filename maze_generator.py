
"""Maze generation module.

This module contains a reusable ``MazeGenerator`` class that can be imported in
other projects.

Basic usage:

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

The generated structure is available through ``generator.grid``.
Each cell stores its walls and whether it belongs to the 42 pattern.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
import random
from typing import Dict, List, Optional, Set, Tuple

Direction = str
Coordinate = Tuple[int, int]

DIRECTIONS: Tuple[Direction, ...] = ("N", "E", "S", "W")
DELTAS: Dict[Direction, Tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}
OPPOSITE: Dict[Direction, Direction] = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E",
}
HEX_BITS: Dict[Direction, int] = {
    "N": 1,
    "E": 2,
    "S": 4,
    "W": 8,
}

PATTERN_42: Tuple[str, ...] = (
    "X..X.XXXX",
    "X..X...X.",
    "XXXX.XXXX",
    "...X.X...",
    "...X.XXXX",
)


class PatternTooSmallError(ValueError):
    """Raised when dimensions are too small for the centered 42 pattern."""


@dataclass
class Cell:
    """Represent one maze cell with walls on cardinal directions."""

    x: int
    y: int
    walls: Dict[Direction, bool] = field(
        default_factory=lambda: {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }
    )
    blocked: bool = False


class MazeGenerator:
    """Generate a maze and expose tools to serialize and solve it.

    The generation algorithm is an iterative recursive-backtracker (depth-first
    search). It naturally generates a perfect maze when ``is_perfect`` is true.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit_: Coordinate,
        is_perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize maze parameters.

        Args:
            width: Number of columns.
            height: Number of rows.
            entry: Entry coordinates as (x, y).
            exit_: Exit coordinates as (x, y).
            is_perfect: Whether to preserve a single-path perfect maze.
            seed: Optional random seed for reproducible generation.
        """
        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers.")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.is_perfect = is_perfect
        self.seed = seed
        self.random = random.Random(seed)

        self.grid: List[List[Cell]] = []
        self.blocked_cells: Set[Coordinate] = set()
        self.warnings: List[str] = []

        self._validate_coordinates(entry, "ENTRY")
        self._validate_coordinates(exit_, "EXIT")
        if entry == exit_:
            raise ValueError("ENTRY and EXIT must be different coordinates.")

    def _validate_coordinates(self, point: Coordinate, key_name: str) -> None:
        """Ensure a coordinate is inside maze bounds."""
        x, y = point
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError(
                f"{key_name} must be inside maze bounds (0..{self.width - 1}, "
                f"0..{self.height - 1})."
            )

    def _build_grid(self) -> None:
        """Create a fresh grid where all walls start closed."""
        self.grid = []
        for y in range(self.height):
            row: List[Cell] = []
            for x in range(self.width):
                row.append(Cell(x=x, y=y))
            self.grid.append(row)

    def _centered_42_cells(self) -> Set[Coordinate]:
        """Compute centered hardcoded 42 pattern cells.

        Raises:
            PatternTooSmallError: If the maze is too small to hold the pattern.
        """
        pattern_height = len(PATTERN_42)
        pattern_width = len(PATTERN_42[0])

        if self.width < pattern_width or self.height < pattern_height:
            raise PatternTooSmallError(
                "Maze too small for centered 42 pattern; "
                "continuing without it."
            )

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        cells: Set[Coordinate] = set()
        for row_index, row_text in enumerate(PATTERN_42):
            for col_index, char in enumerate(row_text):
                if char == "X":
                    cells.add((start_x + col_index, start_y + row_index))
        return cells

    def _apply_42_pattern(self) -> None:
        """Mark cells of the 42 pattern as blocked with all walls closed."""
        try:
            self.blocked_cells = self._centered_42_cells()
        except PatternTooSmallError as error:
            self.warnings.append(str(error))
            self.blocked_cells = set()
            return

        for x, y in self.blocked_cells:
            cell = self.grid[y][x]
            cell.blocked = True
            for direction in DIRECTIONS:
                cell.walls[direction] = True

    def _validate_entry_exit_not_blocked(self) -> None:
        """Ensure entry and exit are not part of the 42 pattern."""
        if self.entry in self.blocked_cells:
            raise ValueError("ENTRY cannot be inside the 42 pattern.")
        if self.exit in self.blocked_cells:
            raise ValueError("EXIT cannot be inside the 42 pattern.")

    def _neighbors(self, cell: Cell) -> List[Tuple[Direction, Cell]]:
        """Return existing neighbors of a cell with their directions."""
        result: List[Tuple[Direction, Cell]] = []
        for direction, (dx, dy) in DELTAS.items():
            nx = cell.x + dx
            ny = cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                result.append((direction, self.grid[ny][nx]))
        return result

    @staticmethod
    def _open_between(
        cell_a: Cell,
        cell_b: Cell,
        direction_from_a: Direction,
    ) -> None:
        """Open the wall between two adjacent cells."""
        cell_a.walls[direction_from_a] = False
        cell_b.walls[OPPOSITE[direction_from_a]] = False

    def _first_open_cell(self) -> Cell:
        """Return the first non-blocked cell in row-major order."""
        for row in self.grid:
            for cell in row:
                if not cell.blocked:
                    return cell
        raise ValueError("No usable cell left after applying constraints.")

    def _carve_perfect_maze(self) -> None:
        """Generate a perfect maze over non-blocked cells using DFS."""
        start = self._first_open_cell()
        visited: Set[Coordinate] = {(start.x, start.y)}
        stack: List[Cell] = [start]

        while stack:
            current = stack[-1]
            candidates: List[Tuple[Direction, Cell]] = []

            for direction, neighbor in self._neighbors(current):
                point = (neighbor.x, neighbor.y)
                if neighbor.blocked:
                    continue
                if point in visited:
                    continue
                candidates.append((direction, neighbor))

            if not candidates:
                stack.pop()
                continue

            direction, next_cell = self.random.choice(candidates)
            self._open_between(current, next_cell, direction)
            visited.add((next_cell.x, next_cell.y))
            stack.append(next_cell)

        open_cells = self.width * self.height - len(self.blocked_cells)
        if len(visited) != open_cells:
            raise RuntimeError(
                "Maze generation failed to connect all non-blocked cells."
            )

    def generate(self) -> None:
        """Generate a full maze according to configured parameters."""
        self.warnings = []
        self._build_grid()
        self._apply_42_pattern()
        self._validate_entry_exit_not_blocked()
        self._carve_perfect_maze()

    def _open_neighbors(
        self,
        point: Coordinate,
    ) -> List[Tuple[Direction, Coordinate]]:
        """Return neighbors reachable from point through open walls."""
        x, y = point
        cell = self.grid[y][x]
        neighbors: List[Tuple[Direction, Coordinate]] = []

        for direction, (dx, dy) in DELTAS.items():
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                continue
            if cell.walls[direction]:
                continue
            if self.grid[ny][nx].blocked:
                continue
            neighbors.append((direction, (nx, ny)))

        return neighbors

    def shortest_path(self) -> List[Direction]:
        """Return shortest path from entry to exit as N/E/S/W steps."""
        queue: deque[Coordinate] = deque([self.entry])
        parents: Dict[Coordinate, Optional[Coordinate]] = {self.entry: None}
        parent_direction: Dict[Coordinate, Direction] = {}

        while queue:
            current = queue.popleft()
            if current == self.exit:
                break

            for direction, neighbor in self._open_neighbors(current):
                if neighbor in parents:
                    continue
                parents[neighbor] = current
                parent_direction[neighbor] = direction
                queue.append(neighbor)

        if self.exit not in parents:
            raise RuntimeError("No valid path exists between ENTRY and EXIT.")

        steps: List[Direction] = []
        cursor = self.exit
        while cursor != self.entry:
            direction = parent_direction[cursor]
            steps.append(direction)
            parent = parents[cursor]
            if parent is None:
                break
            cursor = parent

        steps.reverse()
        return steps

    def path_cells(self, steps: List[Direction]) -> Set[Coordinate]:
        """Convert a direction list into traversed coordinates."""
        visited: Set[Coordinate] = {self.entry}
        x, y = self.entry

        for direction in steps:
            dx, dy = DELTAS[direction]
            x += dx
            y += dy
            visited.add((x, y))

        return visited

    def to_hex_rows(self) -> List[str]:
        """Serialize maze walls as hexadecimal rows."""
        rows: List[str] = []

        for row in self.grid:
            chars: List[str] = []
            for cell in row:
                value = 0
                for direction in DIRECTIONS:
                    if cell.walls[direction]:
                        value += HEX_BITS[direction]
                chars.append(format(value, "X"))
            rows.append("".join(chars))

        return rows
