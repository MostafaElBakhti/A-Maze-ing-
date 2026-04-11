"""ASCII visualization helpers for generated mazes."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from maze_generator import MazeGenerator

Coordinate = Tuple[int, int]

RESET = "\033[0m"
PALETTES: List[Dict[str, str]] = [
    {
        "wall": "\033[97m",
        "entry": "\033[95m",
        "exit": "\033[91m",
        "path": "\033[96m",
        "pattern": "\033[90m",
        "text": "\033[97m",
    },
    {
        "wall": "\033[93m",
        "entry": "\033[94m",
        "exit": "\033[91m",
        "path": "\033[92m",
        "pattern": "\033[37m",
        "text": "\033[93m",
    },
    {
        "wall": "\033[92m",
        "entry": "\033[96m",
        "exit": "\033[91m",
        "path": "\033[94m",
        "pattern": "\033[97m",
        "text": "\033[92m",
    },
]


class AsciiVisualizer:
    """Render mazes in terminal using simple ASCII blocks."""

    def __init__(
        self,
        generator: MazeGenerator,
        path_steps: List[str],
    ) -> None:
        """Initialize visualizer with current maze state and path."""
        self.generator = generator
        self.path_steps = path_steps

    @staticmethod
    def _colorize(text: str, color_code: str) -> str:
        """Wrap text in an ANSI color sequence."""
        return f"{color_code}{text}{RESET}"

    def _path_cells(self) -> Set[Coordinate]:
        """Return coordinates visited by shortest path."""
        return self.generator.path_cells(self.path_steps)

    def _cell_content(
        self,
        point: Coordinate,
        show_path: bool,
        path_cells: Set[Coordinate],
    ) -> str:
        """Return a 3-character content block for one cell."""
        if point == self.generator.entry:
            return " E "
        if point == self.generator.exit:
            return " F "

        x_coord, y_coord = point
        cell = self.generator.grid[y_coord][x_coord]
        if cell.blocked:
            return "XXX"
        if show_path and point in path_cells:
            return " . "
        return "   "

    def render_lines(self, show_path: bool = False) -> List[str]:
        """Build boxed ASCII walls before color formatting."""
        path_cells = self._path_cells() if show_path else set()
        lines: List[str] = []

        for y_index, row in enumerate(self.generator.grid):
            top_parts: List[str] = []
            for cell in row:
                top_parts.append("+")
                if cell.walls["N"]:
                    top_parts.append("---")
                else:
                    top_parts.append("   ")
            top_parts.append("+")
            lines.append("".join(top_parts))

            middle_parts: List[str] = []
            for cell in row:
                if cell.walls["W"]:
                    middle_parts.append("|")
                else:
                    middle_parts.append(" ")

                point = (cell.x, y_index)
                middle_parts.append(
                    self._cell_content(
                        point=point,
                        show_path=show_path,
                        path_cells=path_cells,
                    )
                )

            if row[-1].walls["E"]:
                middle_parts.append("|")
            else:
                middle_parts.append(" ")

            lines.append("".join(middle_parts))

        bottom_parts: List[str] = []
        for cell in self.generator.grid[-1]:
            bottom_parts.append("+")
            if cell.walls["S"]:
                bottom_parts.append("---")
            else:
                bottom_parts.append("   ")
        bottom_parts.append("+")
        lines.append("".join(bottom_parts))

        return lines

    def _apply_color_palette(
        self,
        lines: List[str],
        palette_index: int,
    ) -> List[str]:
        """Apply colors to rendered lines using selected palette."""
        palette = PALETTES[palette_index % len(PALETTES)]
        colored: List[str] = []

        for line in lines:
            pieces: List[str] = []
            for char in line:
                if char in "+-|":
                    pieces.append(self._colorize(char, palette["wall"]))
                elif char == "E":
                    pieces.append(self._colorize(char, palette["entry"]))
                elif char == "F":
                    pieces.append(self._colorize(char, palette["exit"]))
                elif char == ".":
                    pieces.append(self._colorize(char, palette["path"]))
                elif char == "X":
                    pieces.append(self._colorize(char, palette["pattern"]))
                else:
                    pieces.append(char)
            colored.append("".join(pieces))

        return colored

    def display(
        self,
        show_path: bool,
        palette_index: int,
        generation_seed: int | None,
        warnings: List[str],
    ) -> None:
        """Print maze rendering and status text to terminal."""
        palette = PALETTES[palette_index % len(PALETTES)]

        print()
        print(self._colorize("A-Maze-ing", palette["text"]))
        if generation_seed is None:
            print("Seed: random")
        else:
            print(f"Seed: {generation_seed}")

        for warning in warnings:
            print(self._colorize(f"Warning: {warning}", "\033[93m"))

        print()
        lines = self.render_lines(show_path=show_path)
        for line in self._apply_color_palette(lines, palette_index):
            print(line)
        print()
