Point = tuple[int, int]
Scores = dict[Point, int]


def parse(input: str, verbose: bool) -> list[Point]:
    return [(int(line.split(',')[0]), int(line.split(',')[1])) for line in input.split('\n')]


def neighbors(point: Point) -> list[Point]:
    x, y = point
    return [
        (x, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
    ]


def find_exit_path(obstacles: list[Point], start: Point, end: Point) -> int:
    next_points = [(start, 0)]
    best_scores: Scores = {start: 0}
    while next_points:
        point, score = next_points.pop(0)
        if point == end:
            continue
        for neighbor in neighbors(point):
            x, y = neighbor
            if x < start[0] or y < start[1] or x > end[0] or y > end[1]:
                continue
            if neighbor in obstacles:
                continue
            neighbor_score = score + 1

            if best_scores.get(neighbor, neighbor_score + 1) <= neighbor_score:
                continue
            best_scores[neighbor] = neighbor_score
            next_points.append((neighbor, neighbor_score))
    best_end = best_scores.get(end, -1)
    return best_end


def solve_A(input: str, verbose: bool = False) -> int:
    obstacles = parse(input, verbose)
    obstacles = obstacles[:1024] if not verbose else obstacles[:12]
    start = (0, 0)
    end = (70, 70) if not verbose else (6, 6)
    return find_exit_path(obstacles, start, end)


def solve_B(input: str, verbose: bool = False) -> str:
    obstacles = parse(input, verbose)
    start = (0, 0)
    end = (70, 70) if not verbose else (6, 6)

    low = 0
    high = len(obstacles)
    while low < high:
        mid = (low + high) // 2
        if find_exit_path(obstacles[:mid], start, end) >= 0:
            low = mid + 1
        else:
            high = mid
    blocking_obstacle = obstacles[low - 1]
    return f"{blocking_obstacle[0]},{blocking_obstacle[1]}"

