import sys

Point = tuple[int, int]

class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> list[Point]:
    lines = input.split('\n')
    points = [line.split(',') for line in lines]
    points = [(int(i), int(j)) for i, j in points]
    if verbose:
        print('PARSED:')
        print(points)
    return points


def area(a: Point, b: Point) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def diag_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def closest_corner_points(corner: Point, points: list[Point]) -> list[Point]:
    points_from_corner = sorted(points, key=lambda p: diag_dist(p, corner))
    smallest_area = diag_dist(points_from_corner[0], corner)
    corner_points = []
    for p in points_from_corner:
        if diag_dist(p, corner) > smallest_area:
            break
        corner_points.append(p)
    return corner_points


def solve_A(input: str, verbose: bool = True) -> int:
    points = parse(input, verbose)

    edge_left, edge_top = edge_right, edge_bottom = points[0]
    for i, j in points:
        edge_top = min(j, edge_top)
        edge_bottom = max(j, edge_bottom)
        edge_left = min(i, edge_left)
        edge_right = max(i, edge_right)

    if verbose:
        print(f'Field size: {edge_left} -> {edge_right} x {edge_top} -> {edge_bottom}')

    corner_tl = closest_corner_points((edge_left, edge_top), points)
    corner_tr = closest_corner_points((edge_right, edge_top), points)
    corner_bl = closest_corner_points((edge_left, edge_bottom), points)
    corner_br = closest_corner_points((edge_right, edge_bottom), points)

    max_area = 0
    for a in corner_tl:
        for b in corner_br:
            max_area = max(area(a, b), max_area)
    for a in corner_tr:
        for b in corner_bl:
            max_area = max(area(a, b), max_area)

    if verbose:
        print(max_area)
    return max_area


def solve_B(input: str, verbose: bool = False) -> int:
    points = parse(input, verbose)

    def next_point(idx: int) -> Point:
        next_idx = (idx + 1) % len(points)
        return points[next_idx]

    anti_clockwise_border = set()
    clockwise_border = set()
    edges = set()
    for idx, p in enumerate(points):
        next_p = next_point(idx)

        left = min(p[0], next_p[0])
        right = max(p[0], next_p[0])
        top = min(p[1], next_p[1])
        bottom = max(p[1], next_p[1])

        if top != bottom:
            is_clockwise = p[1] < next_p[1]
            for j in range(top, bottom + 1):
                edges.add((p[0], j))
                if is_clockwise:
                    clockwise_border.add((p[0] + 1, j))
                    anti_clockwise_border.add((p[0] - 1, j))
                else:
                    clockwise_border.add((p[0] - 1, j))
                    anti_clockwise_border.add((p[0] + 1, j))
        elif left != right:
            is_clockwise = p[0] < next_p[0]
            for i in range(left, right + 1):
                edges.add((i, p[1]))
                if is_clockwise:
                    clockwise_border.add((i, p[1] - 1))
                    anti_clockwise_border.add((i, p[1] + 1))
                else:
                    clockwise_border.add((i, p[1] + 1))
                    anti_clockwise_border.add((i, p[1] - 1))

    anti_clockwise_border.difference_update(edges)
    clockwise_border.difference_update(edges)

    if len(clockwise_border) > len(anti_clockwise_border):
        border = clockwise_border
    else:
        border = anti_clockwise_border

    points_set = set(points)
    i_range = set([i for i, _ in points])
    j_range = set([j for _, j in points])

    border_i_list = sorted(set([i for i, _ in border if i not in i_range]))
    border_j_list = sorted(set([j for _, j in border if j not in j_range]))
    prev_i: int | None = None
    for i in border_i_list:
        if prev_i is None or i > prev_i + 1:
            i_range.add(i)
        prev_i = i
    prev_j: int | None = None
    for j in border_j_list:
        if prev_j is None or j > prev_j + 1:
            j_range.add(j)
        prev_j = j

    max_area = 0
    for idx, p in enumerate(points):
        border_left: int | None = None
        border_right: int | None = None
        border_bottom: int | None = None
        shift = 0
        while not (border_left and border_right and border_bottom):
            shift += 1
            if border_right is None and (p[0] + shift, p[1]) in border:
                border_right = p[0] + shift
            if border_left is None and (p[0] - shift, p[1]) in border:
                border_left = p[0] - shift
            if border_bottom is None and (p[0], p[1] + shift) in border:
                border_bottom = p[1] + shift

        theoretical_max_area = max(
            (border_right - p[0]) * (border_bottom - p[1]),
            (p[0] - border_left) * (border_bottom - p[1])
        )
        if theoretical_max_area < max_area:
            continue

        for j in range(p[1], border_bottom):
            if not j in j_range:
                continue
            for i in range(p[0], border_right):
                if not i in i_range:
                    continue
                if (i, j) in points_set:
                    max_area = max(max_area, area(p, (i, j)))
                elif (i, j) in border:
                    border_right = i
                    break
            for i in range(p[0] - 1, border_left, -1):
                if not i in i_range:
                    continue
                if (i, j) in points_set:
                    max_area = max(max_area, area(p, (i, j)))
                elif (i, j) in border:
                    border_left = i
                    break

    return max_area
