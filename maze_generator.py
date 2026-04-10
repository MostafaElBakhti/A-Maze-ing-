

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            'N': True,
            'S': True,
            'E': True,
            'W': True
        }
        self.visited = False


def generate_maze(width, height):

    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)

    return grid

def get_neighbors(cell, grid):
    neighbors = {}
    width = len(grid[0])
    height = len(grid)

    x, y = cell.x, cell.y

    if y > 0:
        neighbors["N"] = grid[y-1][x]
    if x < width - 1:
        neighbors["E"] = grid[y][x+1]
    if y < height - 1:
        neighbors["S"] = grid[y+1][x]
    if x > 0:
        neighbors["W"] = grid[y][x-1]

    return neighbors

OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

def open_wall(cell, neighbor, direction):
    cell.walls[direction] = False
    neighbor.walls[OPPOSITE[direction]] = False


grid = generate_maze(3, 3)

for row in grid:
    print([f"({cell.x}, {cell.y})" for cell in row])

cell = grid[0][0]
neighbor  = grid[0][1]

print(cell.walls)
print(neighbor.walls)
open_wall(cell, neighbor, "E")
print()
print(cell.walls)
print(neighbor.walls)

# neighbors = get_neighbors(cell, grid)
# print(f"Neighbors of (0, 0): {list(neighbors.keys())}")
# for dir, nei in neighbors.items():
#     print(f"Direction: {dir}, Neighbor: ({nei.x}, {nei.y})")