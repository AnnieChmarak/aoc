from typing import Optional
from fractions import Fraction

CoordXYZ = tuple[float, float, float]
Hailstone = tuple[CoordXYZ, CoordXYZ]


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool = False) -> list[Hailstone]:
    hailstones = []
    for line in input.split('\n'):
        position, velocity = line.split(' @ ')
        position = position.split(', ')
        velocity = velocity.split(', ')
        hailstones.append(((int(position[0]), int(position[1]), int(position[2])),
                           (int(velocity[0]), int(velocity[1]), int(velocity[2]))))
    return hailstones


def _intersectXY(hail1: Hailstone, hail2: Hailstone) -> Optional[CoordXYZ]:
    pos1, vel1 = hail1
    pos2, vel2 = hail2

    x1, y1, _ = pos1
    dx1, dy1, _ = vel1
    x2, y2, _ = pos2
    dx2, dy2, _ = vel2

    determinant = dx1 * dy2 - dy1 * dx2
    if determinant == 0:
        # Rays are parallel, no intersection
        return None

    t1 = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / determinant
    t2 = ((x2 - x1) * dy1 - (y2 - y1) * dx1) / determinant
    if t1 >= 0 and t2 >= 0:
        intersection_x = x1 + t1 * dx1
        intersection_y = y1 + t1 * dy1
        return intersection_x, intersection_y, -1
    else:
        return None
    

def _solve_system(coeffs: list, results: list) -> Optional[list]:
    N = len(coeffs)
    unknowns = [0 for _ in range(N)]
    for i in range(N):
        max_idx = -1
        max_coeff = 0.0
        for j in range(i, N):
            if abs(coeffs[j][i]) > max_coeff:
                max_coeff = abs(coeffs[j][i])
                max_idx = j

        if round(max_coeff) == 0:
            return None
        results[i], results[max_idx] = results[max_idx], results[i]
        for j in range(N):
            coeffs[i][j], coeffs[max_idx][j] = coeffs[max_idx][j], coeffs[i][j]
        
        for j in range(i+1, N):
            reduced = coeffs[j][i] / coeffs[i][i]
            for k in range(i, N):
                coeffs[j][k] -= reduced * coeffs[i][k]
            results[j] -= reduced * results[i]

    for i in reversed(range(N)):
        unknowns[i] = results[i]
        for j in range(i+1, N):
            unknowns[i] -= coeffs[i][j] * unknowns[j]
        unknowns[i] /= coeffs[i][i]
    return unknowns


def solve_A(input: str, verbose: bool = False) -> int:
    hailstones = parse(input, verbose)
    N = len(hailstones)

    def _is_within_area(point: CoordXYZ):
        test_area = range(200000000000000, 400000000000000 + 1)
        return round(point[0] - 0.5) in test_area and \
            round(point[0] + 0.5) in test_area and \
            round(point[1] - 0.5) in test_area and \
            round(point[1] + 0.5) in test_area

    cross_inside_test_area = 0
    for i in range(N):
        for j in range(i + 1, N):
            cross = _intersectXY(hailstones[i], hailstones[j])
            if verbose:
                print(f'{hailstones[i]} x {hailstones[j]} = {cross}')
            if cross and _is_within_area(cross):
                cross_inside_test_area += 1

    return cross_inside_test_area


def solve_B(input: str, verbose: bool = False) -> int:
    hailstones = parse(input, verbose)

    rock = None
    shift = 0
    while not rock:
        h1, h2, h3 = [hailstones[i] for i in range(shift, shift + 3)]
        (p1, v1), (p2, v2), (p3, v3) = h1, h2, h3

        coeffs = [
            [v1[1] - v2[1], v2[0] - v1[0], 0.0,           p2[1] - p1[1], p1[0] - p2[0], 0.0          ],
            [v1[1] - v3[1], v3[0] - v1[0], 0.0,           p3[1] - p1[1], p1[0] - p3[0], 0.0          ],
            [v1[2] - v2[2], 0.0          , v2[0] - v1[0], p2[2] - p1[2], 0.0,           p1[0] - p2[0]],
            [v1[2] - v3[2], 0.0          , v3[0] - v1[0], p3[2] - p1[2], 0.0,           p1[0] - p3[0]],
            [0.0,           v1[2] - v2[2], v2[1] - v1[1], 0.0,           p2[2] - p1[2], p1[1] - p2[1]],
            [0.0,           v1[2] - v3[2], v3[1] - v1[1], 0.0,           p3[2] - p1[2], p1[1] - p3[1]],
        ]
        results = [
            p2[1]*v2[0] - p2[0]*v2[1] - p1[1]*v1[0] + p1[0]*v1[1],
            p3[1]*v3[0] - p3[0]*v3[1] - p1[1]*v1[0] + p1[0]*v1[1],
            p2[2]*v2[0] - p2[0]*v2[2] - p1[2]*v1[0] + p1[0]*v1[2],
            p3[2]*v3[0] - p3[0]*v3[2] - p1[2]*v1[0] + p1[0]*v1[2],
            p2[2]*v2[1] - p2[1]*v2[2] - p1[2]*v1[1] + p1[1]*v1[2],
            p3[2]*v3[1] - p3[1]*v3[2] - p1[2]*v1[1] + p1[1]*v1[2],
        ]

        rock = _solve_system(coeffs, results)
        shift += 3
        
    print(rock)
    print(rock[0] + rock[1] + rock[2])

    return round(rock[0] + rock[1] + rock[2])