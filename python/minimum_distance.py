import collections
from pprint import pprint

FLAT = 1
TRENCH = 0
OBSTACLE = 9
MOVEMENTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
START_POSITION = (0, 0)


def is_valid_position(grid, number_of_rows, number_of_columns, position):
    return 0 <= position[0] < number_of_columns and 0 <= position[1] < number_of_rows


def get_neighbors(grid, number_of_rows, number_of_columns, origin):
    neighbors = []

    for movement in MOVEMENTS:
        position = (origin[0] + movement[0], origin[1] + movement[1])
        if is_valid_position(grid, number_of_rows, number_of_columns, position):
            neighbors.append(position)

    return neighbors


def bfs(grid, number_of_rows, number_of_columns, start_position, goal):
    queue = collections.deque([[start_position]])
    visited = set([start_position])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        neighbors = get_neighbors(grid, number_of_rows, number_of_columns, (x, y))
        for nx, ny in neighbors:
            if grid[ny][nx] != TRENCH and (nx, ny) not in visited:
                queue.append(path + [(nx, ny)])
                visited.add((nx, ny))


def removeObstacle(numRows, numColumns, lot):
    return len(bfs(lot, numRows, numColumns, START_POSITION, OBSTACLE)) - 1


grid = [
    [FLAT, TRENCH, TRENCH, FLAT],
    [FLAT, TRENCH, TRENCH, FLAT],
    [FLAT, OBSTACLE, FLAT, FLAT],
    [FLAT, FLAT, FLAT, FLAT],
]

def generate_tile():
    return

new_grid: list = []

for i in range(10):
    new_grid.append([])
    for j in range(10):
        new_grid[i].append(generate_tile())

pprint(new_grid)

# number_of_rows = 3
# number_of_columns = 3

# print(get_neighbors(grid, number_of_rows, number_of_columns, START_POSITION))

# pprint(grid, width=40)

# pprint(bfs(grid, number_of_rows, number_of_columns, (0, 0), OBSTACLE))
