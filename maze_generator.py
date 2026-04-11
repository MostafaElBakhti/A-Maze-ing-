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


def generate_maze(width, height, seed=None):

    if seed is not None:
        random.seed(seed)

    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)

    return grid

grid = generate_maze(20, 9, seed=None)

# for row in grid:
#     print([f"({cell.x}, {cell.y})" for cell in row])

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


# grid = generate_maze(13, 10, seed=42)
cell = grid[0][0]
cell.visited = True

stack = [cell]

while stack:
    current = stack[-1]

    unvisited = get_unvisited_neighbors(current, grid)

    if unvisited:
        direction, next_cell = random.choice(list(unvisited.items()))
        open_wall(current, next_cell, direction)
        next_cell.visited = True
        stack.append(next_cell)
    else:
        stack.pop()



def print_maze(grid):
    width = len(grid[0])
    height = len(grid)

    # top border
    print("+" + "---+" * width)

    for y in range(height):
        # walls (vertical)
        row = "|"
        for x in range(width):
            cell = grid[y][x]
            if cell.walls["E"]:
                row += "   |"
            else:
                row += "    "
        print(row)

        # bottom walls
        row = "+"
        for x in range(width):
            cell = grid[y][x]
            if cell.walls["S"]:
                row += "---+"
            else:
                row += "   +"
        print(row)


print_maze(grid)

# unvisited = get_unvisited_neighbors(cell, grid)
# print(f"unvisited neighbors of (0, 0): {list(unvisited.keys())}")

# cell = grid[0][1]

# unvisited = get_unvisited_neighbors(cell, grid)
# print(f"unvisited neighbors of (0, 1): {list(unvisited.keys())}")
# cell.visited = True
# cell = grid[1][1]
# unvisited = get_unvisited_neighbors(cell, grid)
# print(f"unvisited neighbors of (1, 1): {list(unvisited.keys())}")
# grid = generate_maze(3, 3)

# https://www.youtube.com/watch?v=zyQxzMa_DtQ&t=1811s   50min

