Point = tuple[int, int]
Field = list[list[chr]]
Scores = dict[tuple[Point, chr], int]


def parse(input: str, verbose: bool) -> tuple[Field, Point, Point]:
    field = [[c for c in line] for line in input.split('\n')]
    start = None
    end = None
    for y, row in enumerate(field):
        for x, c in enumerate(row):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)
    return field, start, end


def neighbors(point: Point, direction: chr) -> list[tuple[Point, chr]]:
    x, y = point
    all_neighbors = [
        ((x, y - 1), '^'),
        ((x - 1, y), '<'),
        ((x + 1, y), '>'),
        ((x, y + 1), 'v'),
    ]
    if direction == '^':
        return [n for n in all_neighbors if n[1] != 'v']
    if direction == 'v':
        return [n for n in all_neighbors if n[1] != '^']
    if direction == '<':
        return [n for n in all_neighbors if n[1] != '>']
    if direction == '>':
        return [n for n in all_neighbors if n[1] != '<']
    assert False, f"Unknown direction: {direction}"


def solve_A(input: str, verbose: bool = False) -> int:
    field, start, end = parse(input, verbose)
    next_points = [(start, '>', 0)]
    best_scores: Scores = {(start, '>'): 0}
    while next_points:
        point, direction, score = next_points.pop(0)
        if point == end:
            continue
        for neighbor, neighbor_direction in neighbors(point, direction):
            x, y = neighbor
            c = field[y][x]
            if c == '#':
                continue
            neighbor_score = score + 1
            if direction != neighbor_direction:
                neighbor_score += 1000

            if best_scores.get((neighbor, neighbor_direction), neighbor_score + 1) <= neighbor_score:
                continue
            best_scores[(neighbor, neighbor_direction)] = neighbor_score
            next_points.append((neighbor, neighbor_direction, neighbor_score))
    best_end = min(best_scores.get((end, d), 1000000) for d in '^v<>')
    return best_end


def solve_B(input: str, verbose: bool = False) -> int:
    field, start, end = parse(input, verbose)
    next_points = [(start, '>', 0)]
    best_scores: Scores = {(start, '>'): 0}
    best_paths: dict[tuple[Point, chr], set[Point]] = {(start, '>'): set()}
    while next_points:
        point, direction, score = next_points.pop(0)
        if point == end:
            continue
        for neighbor, neighbor_direction in neighbors(point, direction):
            x, y = neighbor
            c = field[y][x]
            if c == '#':
                continue
            neighbor_score = score + 1
            if direction != neighbor_direction:
                neighbor_score += 1000

            point_path = best_paths[(point, direction)].copy()
            best_score = best_scores.get((neighbor, neighbor_direction), neighbor_score + 1)
            if best_score < neighbor_score:
                continue
            if best_score > neighbor_score:
                best_paths[(neighbor, neighbor_direction)] = set()
            best_paths[(neighbor, neighbor_direction)].update(point_path)
            best_paths[(neighbor, neighbor_direction)].add(point)
            if best_score and best_score == neighbor_score:
                continue
            best_scores[(neighbor, neighbor_direction)] = neighbor_score
            next_points.append((neighbor, neighbor_direction, neighbor_score))
    all_end_path_len = 0
    for d in '^v<>':
        all_end_path_len = max(all_end_path_len, len(best_paths.get((end, d), set())))
    return all_end_path_len + 1
