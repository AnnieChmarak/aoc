Matrix = list[list[int]]
Point = tuple[int, int]
PointToStart = dict[Point, set[Point]]
PointToScore = dict[Point, int]


def parse(input: str, verbose: bool) -> Matrix:
    field: Matrix = []

    def safe_int(c: str) -> int:
        return int(c) if c != '.' else -1

    for line in input.split('\n'):
        field.append([safe_int(c) for c in line])
    return field


def neighbors(point: Point, field: Matrix) -> list[Point]:
    i, j = point
    N, M = len(field), len(field[0])
    neighbor_points = []
    if i > 0:
        neighbor_points.append((i - 1, j))
    if i < N - 1:
        neighbor_points.append((i + 1, j))
    if j > 0:
        neighbor_points.append((i, j - 1))
    if j < M - 1:
        neighbor_points.append((i, j + 1))
    return neighbor_points


def solve_A(input: str, verbose: bool = False) -> int:
    field = parse(input, verbose)

    start_points = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 9:
                start_points.append((i, j))

    curr_level: PointToStart = {p: {p} for p in start_points}
    next_level: PointToStart = {}
    for level in range(9, 0, -1):
        for point, start in curr_level.items():
            for neighbor_point in neighbors(point, field):
                if field[neighbor_point[0]][neighbor_point[1]] == level - 1:
                    if neighbor_point not in next_level:
                        next_level[neighbor_point] = set()
                    next_level[neighbor_point].update(start)

        curr_level = next_level
        next_level = {}

    return sum([len(start) for start in curr_level.values()])


def solve_B(input: str, verbose: bool = False) -> int:
    field = parse(input, verbose)

    start_points = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 9:
                start_points.append((i, j))

    curr_level: PointToScore = {p: 1 for p in start_points}
    next_level: PointToScore = {}
    for level in range(9, 0, -1):
        for point, score in curr_level.items():
            for neighbor_point in neighbors(point, field):
                if field[neighbor_point[0]][neighbor_point[1]] == level - 1:
                    if neighbor_point not in next_level:
                        next_level[neighbor_point] = 0
                    next_level[neighbor_point] += score

        curr_level = next_level
        next_level = {}

    return sum(curr_level.values())