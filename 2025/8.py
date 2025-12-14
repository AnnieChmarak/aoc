from collections import deque

Point = tuple[int, int, int]

class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> list[Point]:
    lines = input.split('\n')
    coords = [line.split(',') for line in lines]
    points = [(int(x), int(y), int(z)) for x, y, z in coords]
    if verbose:
        print('PARSED:')
        print(points)
    return points


def dist(a: Point, b: Point) -> int:
    return sum([(a_i - b_i)**2 for a_i, b_i in zip(a, b)])


def build_closest_pairs(points: list[Point]) -> list[tuple[int, int]]:
    points_n = len(points)
    distances: list[tuple[int, int, int]] = []
    for i in range(points_n):
        for j in range(i+1, points_n):
            distances.append((dist(points[i], points[j]), i, j))
    distances.sort(key=lambda d: d[0])
    return [(i, j) for _, i, j, in distances]


def find_circuits(a: Point, b: Point, circuits: deque[set[Point]]) -> tuple[set[Point], set[Point]]:
    a_circuit = b_circuit = None
    for c in circuits:
        if a in c:
            a_circuit = c
        if b in c:
            b_circuit = c
        if a_circuit and b_circuit:
            return a_circuit, b_circuit
    raise NoSolution


def solve_A(input: str, verbose: bool = False) -> int:
    points = parse(input, verbose)

    closest_pairs = build_closest_pairs(points)
    if verbose:
        closest_pairs = closest_pairs[:10]
    else:
        closest_pairs = closest_pairs[:1000]

    circuits: deque[set[Point]] = deque([{p} for p in points])
    for i, j in closest_pairs:
        a_circuit, b_circuit = find_circuits(points[i], points[j], circuits)
        if a_circuit != b_circuit:
            a_circuit |= b_circuit
            circuits.remove(b_circuit)

    circuits_length = [len(c) for c in circuits]
    circuits_length.sort()
    result = circuits_length[-1] * circuits_length[-2] * circuits_length[-3]
    if verbose:
        print(result)
    return result


def solve_B(input: str, verbose: bool = False) -> int:
    points = parse(input, verbose)

    closest_pairs = build_closest_pairs(points)

    circuits: deque[set[Point]] = deque([{p} for p in points])
    farthest_pair = None
    for i, j in closest_pairs:
        a_circuit, b_circuit = find_circuits(points[i], points[j], circuits)
        if a_circuit != b_circuit:
            a_circuit |= b_circuit
            circuits.remove(b_circuit)
        if len(circuits) == 1:
            farthest_pair = (points[i], points[j])
            break

    cable_length = farthest_pair[0][0] * farthest_pair[1][0]
    if verbose:
        print(cable_length)
    return cable_length