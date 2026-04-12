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

grid = generate_maze(15, 7, seed=None)

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

# print(list(neighbor))

def get_unvisited_neighbors(cell , grid):
    neighbors = get_neighbors(cell, grid)

    unvisited = {}

    for direction, neighbor in neighbors.items():
        """means that the neighbor is unvisited == false"""
        if not neighbor.visited: 
            unvisited[direction] = neighbor

    return unvisited


# grid = generate_maze(13, 10, seed=42)
def carve_maze(grid, start_cell):
    cell = start_cell
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


def is_all_visited(grid) -> bool:
    for row in grid:
        for cell in row:
            if not cell.visited:
                return False
    return True


check = is_all_visited(grid)
print(f"All cells visited: {check}")

start = grid[0][0]
carve_maze(grid, start)

check = is_all_visited(grid)
print(f"All cells visited: {check}")



def print_maze(grid):
    width = len(grid[0])
    height = len(grid)

    # ANSI color codes for prettier display
    COLOR_WALL = "\033[94m"      # Blue for walls
    COLOR_PATH = "\033[92m"      # Green for paths
    COLOR_RESET = "\033[0m"      # Reset color
    
    # Unicode box-drawing characters
    TOP_LEFT = "╔"
    TOP_RIGHT = "╗"
    BOT_LEFT = "╚"
    BOT_RIGHT = "╝"
    H_LINE = "═"
    V_LINE = "║"
    CROSS = "╬"
    T_DOWN = "╦"
    T_UP = "╩"
    T_RIGHT = "╠"
    T_LEFT = "╣"
    CELL_OPEN = " "
    CELL_WALL = "█"
    
    # Top border with prettier style
    print(COLOR_WALL + TOP_LEFT + (H_LINE * 3 + T_DOWN) * (width - 1) + H_LINE * 3 + TOP_RIGHT + COLOR_RESET)
    
    for y in range(height):
        # Cell row with vertical walls
        row = COLOR_WALL + V_LINE + COLOR_RESET
        for x in range(width):
            cell = grid[y][x]
            # Cell content (open space)
            row += COLOR_PATH + " • " + COLOR_RESET
            # Right wall of cell
            if cell.walls["E"]:
                row += COLOR_WALL + V_LINE + COLOR_RESET
            else:
                row += " "
        print(row)
        
        # Horizontal wall row
        row = COLOR_WALL + T_RIGHT + COLOR_RESET
        for x in range(width):
            cell = grid[y][x]
            # Bottom wall of cell
            if cell.walls["S"]:
                row += COLOR_WALL + H_LINE * 3 + COLOR_RESET
            else:
                row += COLOR_PATH + "   " + COLOR_RESET
            # Corner/junction
            if x < width - 1:
                row += COLOR_WALL + CROSS + COLOR_RESET
            else:
                row += COLOR_WALL + T_LEFT + COLOR_RESET
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

