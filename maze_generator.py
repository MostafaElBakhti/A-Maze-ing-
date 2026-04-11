import random

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

grid = generate_maze(3, 3)

for row in grid:
    print([f"({cell.x}, {cell.y})" for cell in row])

print("----------------")

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

cell = grid[0][0]
neighbor = get_neighbors(cell, grid)

print(list(neighbor))

def get_unvisited_neighbors(cell , grid):
    neighbors = get_neighbors(cell, grid)

    unvisited = {}

    for direction, neighbor in neighbors.items():
        """means that the neighbor is unvisited == false"""
        if not neighbor.visited: 
            unvisited[direction] = neighbor

    return unvisited

unvisited = get_unvisited_neighbors(cell, grid)
print(f"unvisited neighbors of (0, 0): {list(unvisited.keys())}")

cell = grid[0][1]

unvisited = get_unvisited_neighbors(cell, grid)
print(f"unvisited neighbors of (0, 1): {list(unvisited.keys())}")
cell.visited = True
cell = grid[1][1]
unvisited = get_unvisited_neighbors(cell, grid)
print(f"unvisited neighbors of (1, 1): {list(unvisited.keys())}")
# grid = generate_maze(3, 3)

# for row in grid:
#     print([f"({cell.x}, {cell.y})" for cell in row])

# cell = grid[0][0]
# neighbor  = grid[0][1]

# print(cell.walls)
# print(neighbor.walls)
# open_wall(cell, neighbor, "E")
# print()
# print(cell.walls)
# print(neighbor.walls)
# print("----------------")
# neighbors = get_neighbors(cell, grid)
# print(list(neighbors))
# print(f"Neighbors of (1, 0): {list(neighbors.keys())}")
# for dir, nei in neighbors.items():
#     print(f"Direction: {dir}, Neighbor: ({nei.x}, {nei.y})")

# cell.visited = True

# for row in grid:
#     for cell in row:
#         print(f"{cell.visited}")


    # def get_invisible_neighbors(cell, grid):
    # neighbors = get_neighbors(cell, grid)

    # invisited_neighbors = {}

    # for direction in neighbors: 


