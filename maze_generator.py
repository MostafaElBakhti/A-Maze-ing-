"""Maze generation and solving module."""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field


class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            "N" : True,
            "E" : True,
            "S" : True,
            "W" : True
        }
 
def create_grid(width, height):
    
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x,y))
        grid.append(row)
    return grid 

def get_neighbors(cell, grid):
    neighbors = {}
    width = len(grid[0])
    height = len(grid)
    
    x, y = cell.x, cell.y

    if y > 0:
        neighbors["N"] = grid[y - 1][x]
    if x < width - 1:
        neighbors["E"] 
    if y < height - 1:
        neighbors["S"] = grid[y + 1][x]
    if x > 0:
        neighbors["W"] = grid[y][x - 1]

    return neighbors

grid = create_grid(3, 3)
for row in grid:
    # for c in row:
    #     print([f"({c.x}, {c.y})"])
    print([f"({c.x}, {c.y})" for c in row])

# cell = grid[0][0]
# neighbors = get_neighbors(cell, grid)
# for dir, nei in neighbors.items():
#     print(f"{dir}:  ({nei.x}, ({nei.y}))")























# class MazeGenerator:
#     """Generate, solve, and export a maze."""

#     def __init__(
#         self,
#         width: int,
#         height: int,
#         entry: tuple[int, int],
#         exit: tuple[int, int],
#         perfect: bool = True,
#         seed: int | None = None,
#     ) -> None:
#         """Initialize the maze generator."""

#         self.width = width
#         self.height = height
#         self.entry = entry
#         self.exit = exit
#         self.perfect = perfect
#         self.seed = seed

#         if self.seed is not None:
#             random.seed(self.seed)

#         self.grid: list[list[Cell]] = self._create_grid()
#         self.path_cells: list[tuple[int, int]] = []
#         self.path_directions: str = ""


#     # 2,3

#     def _in_bounds(self, x: int, y: int) -> bool:
#         """Check if coordinates are inside the maze."""
#         # TODO
#         pass

#     def _get_neighbors(self, x: int, y: int) -> list[tuple[int, int, str]]:
#         """Return all valid neighboring cells with their direction."""
#         # TODO
#         pass

#     def _get_unvisited_neighbors(
#         self, x: int, y: int
#     ) -> list[tuple[int, int, str]]:
#         """Return unvisited neighboring cells."""
#         # TODO
#         pass

#     def _opposite(self, direction: str) -> str:
#         """Return the opposite direction."""
#         # TODO
#         pass

#     def _remove_wall(
#         self,
#         x1: int,
#         y1: int,
#         x2: int,
#         y2: int,
#         direction: str,
#     ) -> None:
#         """Remove the wall between two adjacent cells."""
#         # TODO
#         pass

#     def _reset_visited(self) -> None:
#         """Reset all visited flags in the grid."""
#         # TODO
#         pass

#     def generate(self) -> None:
#         """Generate the maze using DFS / Recursive Backtracking."""
#         # TODO:
#         # 1. Start from entry (or random cell)
#         # 2. Mark visited
#         # 3. While stack not empty:
#         #    - get unvisited neighbors
#         #    - if found: choose random, remove wall, mark visited, push
#         #    - else: pop
#         # 4. If not perfect: add extra openings
#         # 5. Reset visited flags
#         pass

#     def _add_extra_openings(self) -> None:
#         """Open extra walls to create loops if maze is not perfect."""
#         # TODO
#         pass

#     def _accessible_neighbors(
#         self, x: int, y: int
#     ) -> list[tuple[int, int, str]]:
#         """Return neighboring cells accessible without crossing walls."""
#         # TODO
#         pass

#     def solve(self) -> str:
#         """Find the shortest path from entry to exit using BFS."""
#         # TODO:
#         # 1. BFS from entry
#         # 2. Track parent of each visited cell
#         # 3. Reconstruct path
#         # 4. Convert to directions
#         # 5. Store in self.path_cells and self.path_directions
#         pass

#     def _reconstruct_path(
#         self,
#         parent: dict[tuple[int, int], tuple[int, int] | None],
#     ) -> list[tuple[int, int]]:
#         """Reconstruct the path from exit to entry."""
#         # TODO
#         pass

#     def _path_to_directions(self, path: list[tuple[int, int]]) -> str:
#         """Convert a coordinate path into N/E/S/W directions."""
#         # TODO
#         pass

#     def _cell_to_hex(self, cell: Cell) -> str:
#         """Convert a cell's walls into a hexadecimal digit."""
#         # TODO
#         pass

#     def export(self, filename: str) -> None:
#         """Export the maze and its shortest path to a file."""
#         # TODO:
#         # 1. Write maze rows as hex
#         # 2. Empty line
#         # 3. Entry
#         # 4. Exit
#         # 5. Shortest path directions
#         pass
