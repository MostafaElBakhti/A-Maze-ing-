import random
from collections import deque

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
        self.locked = False


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

grid = generate_maze(9, 9, seed=None)

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
    # if neighbor.locked:
    #     return
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
        if not neighbor.visited and not neighbor.locked and not cell.locked: 
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


def is_all_non_locked_visited(grid):
    for row in grid:
        for cell in row:
            if not cell.locked and not cell.visited:
                print(f" Not visited: ({cell.x},{cell.y})")
                return False
    return True



def has_3x3_area(grid) -> bool:

    height = len(grid)
    width = len(grid[0])
    
    for y in range(height - 2):
        for x in range(width - 2):
            if is_3x3_open(grid,x,y):
                return True
    
    return False


def is_3x3_open(grid,x,y):
    for dy in range(3):
        for dx in range(3):
            cell = grid[y + dy][x + dx]
            
            if dx < 2 and cell.walls["E"]:
                return False
            if dy < 2 and cell.walls["S"]:
                return False
    return True

def test_open_are(grid) :
    if(has_3x3_area(grid)):
        print("found 3x3 are")
    else:
        print("no 3x3 area found")



def fix_3x3_areas(grid):
    height = len(grid)
    width = len(grid[0])

    for y in range(height - 2):
        for x in range(width - 2):

            if is_3x3_open(grid, x, y):

                cx = x + 1
                cy = y + 1
                center = grid[cy][cx]

                if center.locked:
                    continue

                directions = ["E", "S"]

                random.shuffle(directions)

                for d in directions:
                    nx, ny = cx, cy

                    if d == "E":
                        nx += 1
                    elif d == "S":
                        ny += 1

                    # check bounds
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue

                    neighbor = grid[ny][nx]

                    # locked
                    if neighbor.locked:
                        continue

                    center.walls[d] = True
                    neighbor.walls[OPPOSITE[d]] = True

                    break
# check = is_all_visited(grid)
# print(f"All cells visited: {check}")


# check = is_all_visited(grid)
# print(f"All cells visited: {check}")

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

def place_42(grid):
    height = len(grid)
    width = len(grid[0])

    coords_4 = [
        (0,0),(0,1),(0,2),(1,2),(2,2),(2,3),(2,4)
    ]

    coords_2 = [
        (0,0),(1,0),(2,0),
                (2,1),
        (0,2),(1,2),(2,2),
        (0,3),
        (0,4),(1,4),(2,4)
    ]

    width_4 = 3
    width_2 = 3
    height_p = 5
    gap = 2

    pattern_width = width_4 + gap + width_2  # = 8

    """ calcul padding to center the pattern in the maze """
    padding = (width - pattern_width) // 2


    if padding < 2:
        raise ValueError("Maze too tight for 42 pattern minimum (12, 9)")

    start_x = padding
    start_y = (height - height_p) // 2

    # place 4
    for x, y in coords_4:
        cell = grid[start_y + y][start_x + x]
        close_cell(grid, cell)

    # place 2
    offset_x = width_4 + gap
    for x, y in coords_2:
        cell = grid[start_y + y][start_x + offset_x + x]
        close_cell(grid, cell)


def close_cell(grid, cell):
    height = len(grid)
    width = len(grid[0])

    cell.locked = True

    cell.walls['N'] = True
    cell.walls['S'] = True
    cell.walls['E'] = True
    cell.walls['W'] = True

    x, y = cell.x, cell.y

    if y > 0:
        grid[y-1][x].walls['S'] = True
    if y < height - 1:
        grid[y+1][x].walls['N'] = True
    if x > 0:
        grid[y][x-1].walls['E'] = True
    if x < width - 1:
        grid[y][x+1].walls['W'] = True



WALL_BITS = {
    "N": 1,
    "E": 2,
    "S": 4,
    "W": 8
}

def encode_cell(cell):
    value = 0

    for direction, bit in WALL_BITS.items():
        if cell.walls[direction]:
            value |= bit
    return value



def encode_grid(grid):
    lines = []

    for row in grid:
        line = ""
        for cell in row:
            encoded = encode_cell(cell)
            line += format(encoded, "X")  # hexadecimal representation
        lines.append(line)
    return lines



def write_maze(file, grid):
    lines = encode_grid(grid)
    for line in lines:
        file.write(line + "\n")


def write_entry_exit(file, entry, exit_):
    file.write(f"{entry[0]},{entry[1]}\n")   # ← no space after comma
    file.write(f"{exit_[0]},{exit_[1]}\n")


def write_output(grid, path, output_file, entry, exit_):
    with open(output_file, "w") as file:
        write_maze(file, grid)
        file.write("\n")
        write_entry_exit(file, entry, exit_)
        file.write("\n")
        file.write("".join(path) + "\n")

test_open_are(grid)
# def bfs_path_exists(grid, start, target):
#     queue = deque([start])
#     visited = set()

#     while queue:
#         cell = queue.popleft()

#         if (cell.x, cell.y) in visited:
#             continue
#         visited.add((cell.x, cell.y))

#         """we found the target, path exists"""
#         if cell == target:
#             return True

#         neighbors = get_neighbors(cell, grid)

#         for direction, neighbor in neighbors.items():
            
#             if not cell.walls[direction] and not neighbor.locked:
#                 if (neighbor.x, neighbor.y) not in visited:
#                     queue.append(neighbor)

#     return False

try:
    place_42(grid)
except ValueError as e:
    print(f"Error placing 42 pattern: {e}")



start = grid[0][0]
carve_maze(grid, start)

# while has_3x3_area(grid):
#     fix_3x3_areas(grid)



def check_pattern_strict(grid):
    ok = True

    for row in grid:
        for cell in row:
            if cell.locked:
                for direction, wall in cell.walls.items():
                    if not wall:
                        print(f" OPEN wall at ({cell.x},{cell.y}) -> {direction}")
                        ok = False

    if ok:
        print(" Pattern 42 fully closed")


check_pattern_strict(grid)
print("All NON-LOCKED visited:", is_all_non_locked_visited(grid))

value = encode_grid(grid)
print(f"Encoded maze: {value}")
# entry = grid[0][0]
# exit = grid[len(grid) - 1][len(grid[0]) - 1]

# print("Path exists:", bfs_path_exists(grid, entry, exit))


entry = (0, 0)
exit_ = (8, 8)  # bottom-right corner for 9x9 grid

write_output(grid, ["N", "E", "S"], "maze_test.txt", entry, exit_)
print("Output written to maze_test.txt")
# :::::::::::::::::::: #
# :::::::::::::::::::: #
# :::::::::::::::::::: # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# :::::::::::::::::::: #
# :::::::::::::::::::: # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# :::::::::::::::::::: #
# :::::::::::::::::::: # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# :::::::::::::::::::: #
# :::::::::::::::::::::#
#       Display       #


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
            if cell.locked:
                row += "███"   # 🔥 42 تبان
            else:
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

#ba9i khas 3x3 , perfect , bfs , output file 