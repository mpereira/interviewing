import collections

FLAT = 1
TRENCH = 0
OBSTACLE = 9
MOVEMENTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
START_POSITION = (0, 0)


def is_valid_position(grid, number_of_rows, number_of_columns, position):
    return (
        0 <= position[0] < number_of_rows
        and 0 <= position[1] < number_of_columns
    )


def get_neighbors(grid, number_of_rows, number_of_columns, origin):
    neighbors = []

    for movement in MOVEMENTS:
        position = (origin[0] + movement[0], origin[1] + movement[1])
        if is_valid_position(grid, number_of_rows, number_of_columns, position):
            neighbors.append(position)

    return neighbors


def bfs(grid, number_of_rows, number_of_columns, start_position, goal):
    queue = collections.deque([[start_position]])
    seen = set([start_position])

    while queue:
        path = queue.popleft()
        row, column = path[-1]
        if grid[row][column] == goal:
            return path
        neighbors = get_neighbors(
            grid, number_of_rows, number_of_columns, (row, column)
        )
        for nrow, ncolumn in neighbors:
            if grid[nrow][ncolumn] != TRENCH and (nrow, ncolumn) not in seen:
                queue.append(path + [(nrow, ncolumn)])
                seen.add((nrow, ncolumn))


# Task: implement remove_obstacle().
def remove_obstacle(num_rows, num_columns, lot):
    return len(bfs(lot, num_rows, num_columns, START_POSITION, OBSTACLE)) - 1


grid = [
    [FLAT, TRENCH, FLAT,   FLAT,   FLAT,   FLAT],
    [FLAT, TRENCH, FLAT,   TRENCH, TRENCH, FLAT],
    [FLAT, FLAT,   FLAT,   TRENCH, TRENCH, FLAT],
    [FLAT, TRENCH, TRENCH, TRENCH, TRENCH, FLAT],
    [FLAT, FLAT,   FLAT,   FLAT,   TRENCH, FLAT],
    [FLAT, TRENCH, TRENCH, FLAT,   TRENCH, OBSTACLE],
]


number_of_rows = len(grid)
number_of_columns = len(grid[0])

print(remove_obstacle(number_of_rows, number_of_columns, grid))
