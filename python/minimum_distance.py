import collections
from pprint import pprint

FLAT = 1
TRENCH = 0
OBSTACLE = 9
MOVEMENTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
START_POSITION = (0, 0)


def is_valid_position(grid, number_of_rows, number_of_columns, position):
    return 0 <= position[0] < number_of_rows and 0 <= position[1] < number_of_columns


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
        print("\nstarting")
        print("queue:", queue)
        print("queue len:", len(queue))
        path = queue.popleft()
        x, y = path[-1]
        if grid[x][y] == goal:
            return path
        neighbors = get_neighbors(grid, number_of_rows, number_of_columns, (x, y))
        print("path:", path)
        print((x, y), "neighbors:", neighbors)
        for nx, ny in neighbors:
            if grid[nx][ny] != TRENCH and (nx, ny) not in visited:
                if grid[nx][ny] == FLAT:
                    _value = "flat"
                elif grid[nx][ny] == TRENCH:
                    _value = "trench"
                elif grid[nx][ny] == OBSTACLE:
                    _value = "obstacle"
                else:
                    _value = "?"
                print((nx, ny), "is", _value)
                queue.append(path + [(nx, ny)])
                print("'queue' updated with", path + [(nx, ny)], ":", queue)
                visited.add((nx, ny))
                print("'visited' updated:", visited)


def removeObstacle(numRows, numColumns, lot):
    return len(bfs(lot, numRows, numColumns, START_POSITION, OBSTACLE)) - 1


grid = [
    [FLAT, TRENCH,   FLAT,   FLAT,   FLAT,    FLAT],
    [FLAT, TRENCH,   FLAT,   TRENCH, TRENCH,  FLAT],
    [FLAT, FLAT,     FLAT,   TRENCH, TRENCH,  FLAT],
    [FLAT, TRENCH,   TRENCH, TRENCH, TRENCH,  FLAT],
    [FLAT, FLAT,     FLAT,   FLAT,   TRENCH,  FLAT],
    [FLAT, TRENCH,   TRENCH, FLAT,   TRENCH,  OBSTACLE],
]

def generate_tile():
    return

# new_grid: list = []

# for i in range(10):
#     new_grid.append([])
#     for j in range(10):
#         new_grid[i].append(generate_tile())

# pprint(new_grid)

number_of_rows = len(grid)
number_of_columns = len(grid[0])

# print(get_neighbors(grid, number_of_rows, number_of_columns, (2, 0)))

# pprint(grid, width=40)

pprint(bfs(grid, number_of_rows, number_of_columns, (0, 0), OBSTACLE))
