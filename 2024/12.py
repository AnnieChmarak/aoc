Matrix = list[list[str]]
Point = tuple[int, int]
Perimeter = list[list[Point]]
AreaPerimeter = tuple[set[Point], Perimeter]

DiagonalToSidePoints = {
    0: (0, 2),
    1: (0, 3),
    2: (1, 2),
    3: (1, 3),
}


def parse(input: str, verbose: bool) -> Matrix:
    field: Matrix = []
    for line in input.split('\n'):
        field.append([c for c in line])
    return field


def extend_field(field: Matrix) -> Matrix:
    N, M = len(field), len(field[0])
    new_field = [['.' for _ in range(M + 2)] for _ in range(N + 2)]
    for i in range(N):
        for j in range(M):
            new_field[i + 1][j + 1] = field[i][j]
    return new_field


def neighbors(point: Point) -> tuple[Point, Point, Point, Point]:
    i, j = point
    side_points = (
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
    )
    return side_points


def diag_neighbors(point: Point) -> tuple[Point, Point, Point, Point]:
    i, j = point
    diagonal_points = (
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i + 1, j - 1),
        (i + 1, j + 1),
    )
    return diagonal_points


def find_region(reg_name: str, point: Point, regions: dict[str, list[AreaPerimeter]]) -> int:
    if reg_name not in regions:
        return -1
    for idx, (area, _) in enumerate(regions[reg_name]):
        if point in area:
            return idx
    return -1


def fill_regions(field: Matrix, verbose: bool) -> dict[str, list[AreaPerimeter]]:
    regions: dict[str, list[AreaPerimeter]] = {}
    N, M = len(field), len(field[0])
    field = extend_field(field)
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            reg_name = field[i][j]
            side_points = neighbors((i, j))

            possible_reg_idxs = {find_region(reg_name, (i, j), regions)}
            for s in side_points:
                if field[s[0]][s[1]] == reg_name:
                    possible_reg_idxs.add(find_region(field[s[0]][s[1]], s, regions))
            if -1 in possible_reg_idxs:
                possible_reg_idxs.remove(-1)

            reg_idx = -1
            if len(possible_reg_idxs) == 0:
                if reg_name not in regions:
                    regions[reg_name] = []
                regions[reg_name].append((set(), [[], [], [], []]))
                reg_idx = len(regions[reg_name]) - 1
            elif len(possible_reg_idxs) == 1:
                reg_idx = possible_reg_idxs.pop()
            else:
                area, perimeter = set(), [[], [], [], []]
                for idx in possible_reg_idxs:
                    area2, perimeter2 = regions[reg_name][idx]
                    area |= area2
                    for p in range(4):
                        perimeter[p] += perimeter2[p]
                area.add((i, j))
                regions[reg_name] = [regions[reg_name][x] for x in range(len(regions[reg_name])) if x not in possible_reg_idxs]
                regions[reg_name].append((area, perimeter))
                reg_idx = len(regions[reg_name]) - 1

            area, perimeter = regions[reg_name][reg_idx]
            area.add((i, j))
            for s, (x, y) in enumerate(side_points):
                if field[x][y] == reg_name:
                    area.add((x, y))
                else:
                    perimeter[s].append((x, y))

            if verbose:
                print(f'{reg_name}({i},{j}): {area}, {perimeter}')

            regions[reg_name][reg_idx] = (area, perimeter)
    return regions


def count_sides(perimeter: Perimeter) -> int:
    def count_strikes(points: list[Point], line: int, value: int) -> int:
        if len(points) == 0:
            return 0

        prev_point = points[0]
        strikes = 1
        for p in range(1, len(points)):
            point = points[p]
            same_strike = prev_point[line] == point[line] and prev_point[value] + 1 == point[value]
            if not same_strike:
                strikes += 1
            prev_point = point

        return strikes

    sides = 0
    for p, points in enumerate(perimeter):
        line = int(p >= 2)
        value = int(p < 2)
        points = sorted(points, key=lambda x: (x[line], x[value]))
        sides += count_strikes(points, line, value)
    return sides


def solve_A(input: str, verbose: bool = False) -> int:
    field = parse(input, verbose)
    regions = fill_regions(field, verbose)

    if verbose:
        for reg_name, reg_data in regions.items():
            print(f'{reg_name}:')
            for area, perimeter in reg_data:
                print(f'  {len(area)}, {len(perimeter)} -> {len(area) * len(perimeter)}')

    price = 0
    for reg_name, reg_data in regions.items():
        for area, perimeter in reg_data:
            price += len(area) * sum([len(p) for p in perimeter])
    return price


def solve_B(input: str, verbose: bool = False) -> int:
    field = parse(input, verbose)
    regions = fill_regions(field, verbose)

    discounted_price = 0
    for reg_name, reg_data in regions.items():
        for area, perimeter in reg_data:
            sides = count_sides(perimeter)
            discounted_price += len(area) * sides
    return discounted_price
