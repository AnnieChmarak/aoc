class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[dict, int, int]:
    field = [list(line) for line in input.split('\n')]
    antennas = {}
    for i in range(len(field)):
        for j in range(len(field[i])):
            name = field[i][j]
            if name != '.':
                if name not in antennas:
                    antennas[name] = []
                antennas[name].append((i, j))
    return antennas, len(field), len(field[0])


def get_radius(coord: tuple, N: int, M: int) -> tuple[int, int]:
    i, j = coord
    x = min(i, N - 1 - i)
    y = min(j, M - 1 - j)
    return x, y


def solve_A(input: str, verbose: bool = False) -> int:
    antennas, N, M = parse(input, verbose)
    antiantennas = {}
    for name, coords in antennas.items():
        antiantennas[name] = []
        for a1 in coords:
            x, y = get_radius(a1, N, M)
            for a2 in coords:
                if a1 == a2:
                    continue
                diff_x = a1[0] - a2[0]
                diff_y = a1[1] - a2[1]
                if abs(diff_x) <= x and abs(diff_y) <= y:
                    a3 = (a1[0] + diff_x, a1[1] + diff_y)
                    antiantennas[name].append(a3)

    if verbose:
        print(antiantennas)

    unique_antiantennas = set()
    for name, coords in antiantennas.items():
        for coord in coords:
            unique_antiantennas.add(coord)

    if verbose:
        print(unique_antiantennas)

    return len(unique_antiantennas)


def solve_B(input: str, verbose: bool = False) -> int:
    antennas, N, M = parse(input, verbose)
    all_antennas = set()
    antiantennas = {}
    for name, coords in antennas.items():
        all_antennas.update(coords)
        antiantennas[name] = []
        for a1 in coords:
            x, y = get_radius(a1, N, M)
            for a2 in coords:
                if a1 == a2:
                    continue
                diff_x = a1[0] - a2[0]
                diff_y = a1[1] - a2[1]
                if abs(diff_x) <= x and abs(diff_y) <= y:
                    a3 = (a1[0] + diff_x, a1[1] + diff_y)
                    while a3[0] >= 0 and a3[0] < N and a3[1] >= 0 and a3[1] < M:
                        antiantennas[name].append(a3)
                        a3 = (a3[0] + diff_x, a3[1] + diff_y)

    if verbose:
        print(antiantennas)

    unique_antiantennas = all_antennas.copy()
    for name, coords in antiantennas.items():
        for coord in coords:
            unique_antiantennas.add(coord)

    if verbose:
        for i in range(N):
            for j in range(M):
                if (i, j) in unique_antiantennas:
                    print('#', end='')
                else:
                    print('.', end='')
            print()

    return len(unique_antiantennas)