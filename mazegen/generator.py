import random
from collections import deque
from typing import Any, Optional, TextIO


class MazeGenerator():
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool,
        output_file: str,
        seed: Optional[int] = None
    ) -> None:
        self.width = width
        self.height = height
        self.exit_ = exit_
        self.entry = entry
        self.perfect = perfect
        self.output_file = output_file
        self.seed = seed
        self.opposite = {
            "N": "S",
            "E": "W",
            "S": "N",
            "W": "E"
        }
        self.wall_bits = {
            "N": 1,
            "E": 2,
            "S": 4,
            "W": 8
        }
        self.directions = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0)
        }

    class Cell:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y
            self.visited = False
            self.locked = False
            self.walls = {
                "N": True,
                "E": True,
                "S": True,
                "W": True
            }

    def creat_grid(self) -> list[list[Any]]:
        grid: list[list[Any]] = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(MazeGenerator.Cell(x, y))
            grid.append(row)

        return grid

    def get_neighbors(
        self, cell: Any, grid: list[list[Any]]
    ) -> dict[str, Any]:
        neighbors: dict[str, Any] = {}
        width = self.width
        height = self.height

        x, y = cell.x, cell.y

        if y > 0:
            neighbors["N"] = grid[y - 1][x]
        if x < width - 1:
            neighbors["E"] = grid[y][x + 1]
        if y < height - 1:
            neighbors["S"] = grid[y + 1][x]
        if x > 0:
            neighbors["W"] = grid[y][x - 1]

        return neighbors

    def remove_wall(
        self, cell: Any, neighbor: Any, direction: str
    ) -> None:
        cell.walls[direction] = False
        neighbor.walls[self.opposite[direction]] = False

    def get_unvisited_neighbors(
        self, cell: Any, grid: list[list[Any]]
    ) -> dict[str, Any]:
        neighbors = self.get_neighbors(cell, grid)

        unvisited_neighbors: dict[str, Any] = {}
        for direction in neighbors:
            neighbor = neighbors[direction]
            if (
                not neighbor.visited
                and not neighbor.locked
                and not cell.locked
            ):
                unvisited_neighbors[direction] = neighbor

        return unvisited_neighbors

    def dfs_algo(
        self, cell: Any, grid: list[list[Any]]
    ) -> Optional[Any]:
        unvisited = self.get_unvisited_neighbors(cell, grid)

        if not unvisited:
            return None

        direction = random.choice(list(unvisited.keys()))
        neighbor = unvisited[direction]

        self.remove_wall(cell, neighbor, direction)
        neighbor.visited = True

        return neighbor

    def generate_maze(self, grid: list[list[Any]]) -> None:
        stack = []
        start = grid[0][0]

        start.visited = True
        stack.append(start)

        while stack:
            current = stack[-1]

            next_cell = self.dfs_algo(current, grid)
            if next_cell:
                stack.append(next_cell)
            else:
                stack.pop()

    def has_3x3_open(self, grid: list[list[Any]]) -> bool:
        height = self.height
        width = self.width

        for y in range(height - 2):
            for x in range(width - 2):
                if self.is_3x3_open(grid, x, y):
                    return True
        return False

    def is_3x3_open(
        self, grid: list[list[Any]], x: int, y: int
    ) -> bool:
        for dy in range(3):
            for dx in range(3):
                cell = grid[dy + y][dx + x]

                if dx < 2 and cell.walls["E"]:
                    return False
                if dy < 2 and cell.walls["S"]:
                    return False
        return True

    def fix_3x3_areas(self, grid: list[list[Any]]) -> None:
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.is_3x3_open(grid, x, y):
                    cx, cy = x + 1, y + 1
                    center = grid[cy][cx]

                    if center.locked:
                        continue

                    d = random.choice(["E", "S"])
                    nx = cx + (1 if d == "E" else 0)
                    ny = cy + (1 if d == "S" else 0)

                    neighbor = grid[ny][nx]
                    if neighbor.locked:
                        continue

                    center.walls[d] = True
                    neighbor.walls[self.opposite[d]] = True
                    return

    def is_fully_closed(self, cell: Any) -> bool:
        return all(cell.walls.values())

    def close_cell(
        self, grid: list[list[Any]], x: int, y: int
    ) -> None:
        cell = grid[y][x]
        cell.visited = True
        cell.locked = True
        cell.walls = {"N": True, "E": True, "S": True, "W": True}

        if y > 0:
            grid[y - 1][x].walls["S"] = True
        if y < self.height - 1:
            grid[y + 1][x].walls["N"] = True
        if x > 0:
            grid[y][x - 1].walls["E"] = True
        if x < self.width - 1:
            grid[y][x + 1].walls["W"] = True

    def draw_4(
        self, grid: list[list[Any]], x: int, y: int
    ) -> None:
        coords = [
            (0, 0),
            (0, 1),
            (0, 2), (1, 2), (2, 2),
                            (2, 3),
                            (2, 4)
        ]

        for dx, dy in coords:
            self.close_cell(grid, x + dx, y + dy)

    def draw_2(
        self, grid: list[list[Any]], x: int, y: int
    ) -> None:
        coords = [
            (0, 0), (1, 0), (2, 0),
                            (2, 1),
            (0, 2), (1, 2), (2, 2),
            (0, 3),
            (0, 4), (1, 4), (2, 4)
            ]

        for dx, dy, in coords:
            self.close_cell(grid, x + dx, y + dy)

    def place_42_pattern(self, grid: list[list[Any]]) -> bool:
        pattern_width = 7

        if self.width < 11 or self.height < 9:
            raise ValueError("maze too small for 42 pattern, min is (11,9)")

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - 5) // 2

        self.draw_4(grid, start_x, start_y)
        self.draw_2(grid, start_x + 4, start_y)

        return True

    def encoded_cell(self, cell: Any) -> int:
        value = 0

        for direction, bit in self.wall_bits.items():
            if cell.walls[direction]:
                value |= bit
        return value

    def encode_grid(self, grid: list[list[Any]]) -> list[str]:
        lines = []

        for row in grid:
            line = ""
            for cell in row:
                encoded = self.encoded_cell(cell)
                line += format(encoded, "X")
            lines.append(line)
        return lines

    def write_maze(
        self, file: TextIO, grid: list[list[Any]]
    ) -> None:
        lines = self.encode_grid(grid)
        for line in lines:
            file.write(line + "\n")

    def write_entry_exit(
        self,
        file: TextIO,
        entry: tuple[int, int],
        exit_: tuple[int, int]
    ) -> None:
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit_[0]},{exit_[1]}\n")

    def write_output(
        self, grid: list[list[Any]], path: list[str]
    ) -> None:
        filename = self.output_file
        entry = self.entry
        exit_ = self.exit_

        with open(filename, "w") as file:
            self.write_maze(file, grid)
            file.write("\n")
            self.write_entry_exit(file, entry, exit_)
            file.write("\n")
            if path:
                file.write("".join(path) + "\n")
            else:
                file.write("NO_PATH\n")

    def can_move(
        self, grid: list[list[Any]], x: int, y: int, direction: str
    ) -> bool:
        cell = grid[y][x]

        if cell.walls[direction]:
            return False

        return True

    def bfs_algo(
        self,
        grid: list[list[Any]],
        entry: tuple[int, int],
        exit_: tuple[int, int]
    ) -> Optional[dict[tuple[int, int], Any]]:
        queue: deque[tuple[int, int]] = deque()
        visited: set[tuple[int, int]] = set()
        parent: dict[tuple[int, int], Any] = {}

        queue.append(entry)
        visited.add(entry)

        while queue:
            x, y = queue.popleft()

            if (x, y) == exit_:
                return parent

            for d in self.directions:
                if self.can_move(grid, x, y, d):
                    dx, dy = self.directions[d]
                    nx, ny = x + dx, y + dy

                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = ((x, y), d)
                        queue.append((nx, ny))
        return None

    def reconstruct_path(
        self,
        parent: dict[tuple[int, int], Any],
        entry: tuple[int, int],
        exit_: tuple[int, int]
    ) -> list[str]:

        path = []
        current = exit_

        while current != entry:
            prev, direction = parent[current]
            path.append(direction)
            current = prev

        path.reverse()
        return path

    def shortest_path(self, grid: list[list[Any]]) -> list[str]:
        entry = self.entry
        exit_ = self.exit_
        parent = self.bfs_algo(grid, entry, exit_)

        if parent is None:
            return []
        return self.reconstruct_path(parent, entry, exit_)

    def path_to_coords(
        self, path: list[str]
    ) -> list[tuple[int, int]]:
        entry = self.entry
        coords = [entry]
        x, y = entry

        for d in path:
            dx, dy = self.directions[d]
            x += dx
            y += dy
            coords.append((x, y))

        return coords

    def break_random_walls(
        self, grid: list[list[Any]], pro: float = 0.1
    ) -> None:
        for row in grid:
            for cell in row:

                if self.is_fully_closed(cell):
                    continue

                for direction, (dx, dy) in self.directions.items():
                    nx, ny = cell.x + dx, cell.y + dy

                    if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                        neighbor = grid[ny][nx]

                        if self.is_fully_closed(neighbor):
                            continue

                        if (cell.walls[direction] and random.random() < pro):
                            self.remove_wall(cell, neighbor, direction)

    def init_random(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)

    def validate_params(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")

        ex, ey = self.entry
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError(
                f"Entry {self.entry} is outside the maze "
                f"({self.width}x{self.height})"
            )

        xx, xy = self.exit_
        if not (0 <= xx < self.width and 0 <= xy < self.height):
            raise ValueError(
                f"Exit {self.exit_} is outside the maze "
                f"({self.width}x{self.height})"
            )

        if self.entry == self.exit_:
            raise ValueError("Entry and exit must be different")

    def generate(
        self
    ) -> tuple[Optional[list[list[Any]]], Optional[list[str]]]:
        try:
            self.validate_params()
        except ValueError as e:
            print(f"Error: {e}")
            return None, None

        self.init_random()
        grid = self.creat_grid()

        try:
            self.place_42_pattern(grid)
        except ValueError as e:
            print(f"Warning: {e} — generating maze without 42 pattern")

        entry_cell = grid[self.entry[1]][self.entry[0]]
        exit_cell = grid[self.exit_[1]][self.exit_[0]]

        if entry_cell.locked:
            print(f"Error: Entry {self.entry} is inside the 42 pattern")
            return None, None

        if exit_cell.locked:
            print(f"Error: Exit {self.exit_} is inside the 42 pattern")
            return None, None

        self.generate_maze(grid)

        while self.has_3x3_open(grid):
            self.fix_3x3_areas(grid)

        if not self.perfect:
            self.break_random_walls(grid)

        path = self.shortest_path(grid)
        self.write_output(grid, path)

        return grid, path


def get_maze(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    perfect: bool,
    output_file: str,
    seed: Optional[int] = None
) -> MazeGenerator:
    maze = MazeGenerator(
        width, height, entry, exit_, perfect, output_file, seed
    )
    return maze
