class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool = False) -> list[list[str]]:
    return [list(line) for line in input.split('\n')]


def _tilt(platform: list[list[str]], verbose: bool, dir: str = 'N'):
    if verbose:
        print(dir)
    moving_to_0 = dir == 'N' or dir == 'W'
    rotate = dir == 'W' or dir == 'E'

    N, M = (len(platform), len(platform[0]))
    if rotate:
        N, M = M, N

    available_places, row_range, col_range = {
        True: ([0] * M,     range(0, N),           range(0, M)),
        False: ([N - 1] * M, reversed(range(0, N)), range(0, M)),
    }[moving_to_0]

    for i in row_range:
        for j in col_range:
            idx = j
            if rotate:
                i, j = j, i
            c = platform[i][j]
            if c == 'O':
                dst_i, dst_j = (available_places[idx], j) if not rotate else (i, available_places[idx])

                if verbose:
                    print(f'{i, j} -> {dst_i, dst_j}')
                platform[i][j] = '.'
                platform[dst_i][dst_j] = 'O'
                available_places[idx] += 1 if moving_to_0 else -1
            elif c == '#':
                available_places[idx] = (i + (1 if moving_to_0 else -1)) if not rotate else (j + (1 if moving_to_0 else -1))

            if rotate:
                i, j = j, i
        if verbose:
            print(available_places)

    if verbose:
        for line in platform:
            print(''.join(c for c in line))
        print()


def _count_load(platform: list[list[str]]) -> int:
    load = 0
    N = len(platform)
    for i in range(0, N):
        load += platform[i].count('O') * (N - i)
    return load


def _hash(platform: list[list[str]]) -> tuple:
    return tuple(tuple(line) for line in platform)


def _unhash(platform_hash: tuple) -> list[list[str]]:
    return [list(line_hash) for line_hash in platform_hash]


def solve_A(input: str, verbose: bool = False) -> int:
    platform = parse(input, verbose)

    _tilt(platform, verbose)

    return _count_load(platform)


def solve_B(input: str, verbose: bool = False) -> int:
    platform = parse(input, verbose)

    seen_platforms = []
    loop_idx = -1

    cycles = 1000000000
    for i in range(cycles):
        platform_hash = _hash(platform)
        try:
            loop_idx = seen_platforms.index(platform_hash)
            if verbose:
                print(f'Cycle {i}, load={_count_load(platform)} repeats cycle #{loop_idx + 1}')
            break
        except ValueError:
            seen_platforms.append(platform_hash)

        for dir in ['N', 'W', 'S', 'E']:
            _tilt(platform, False, dir)

        if verbose:
            print(f'Cycle {i + 1}, load={_count_load(platform)}')

    loop_length = len(seen_platforms) - loop_idx
    platform = _unhash(seen_platforms[loop_idx + ((cycles - len(seen_platforms)) % loop_length)])

    return _count_load(platform)