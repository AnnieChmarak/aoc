import copy


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[dict, dict, tuple]:
    field = [list(line) for line in input.split('\n')]
    blocks_i = dict()
    blocks_j = dict()
    start = None
    for i in range(len(field)):
        for j in range(len(field[i])):
            if i not in blocks_i:
                blocks_i[i] = []
            if j not in blocks_j:
                blocks_j[j] = []

            if field[i][j] == '^':
                start = (i, j)
            elif field[i][j] == '#':
                blocks_i[i].append(j)
                blocks_j[j].append(i)
    return blocks_i, blocks_j, start


def block_before(blocks: list[int], x: int) -> int:
    for y in range(x - 1, -1, -1):
        if y in blocks:
            return y
    return -1


def block_after(blocks: list[int], x: int, max: int) -> int:
    for y in range(x + 1, max):
        if y in blocks:
            return y
    return max


def _step(blocks_i: dict, blocks_j: dict, i: int, j: int, direction: str) -> tuple:
    N, M = len(blocks_i), len(blocks_j)
    next_i, next_j = i, j
    next_direction = None
    if direction == '^':
        next_i = block_before(blocks_j[j], i) + 1
        if next_i != 0:
            next_direction = '>'
    elif direction == '>':
        next_j = block_after(blocks_i[i], j, M) - 1
        if next_j != M - 1:
            next_direction = 'v'
    elif direction == 'v':
        next_i = block_after(blocks_j[j], i, N) - 1
        if next_i != N - 1:
            next_direction = '<'
    elif direction == '<':
        next_j = block_before(blocks_i[i], j) + 1
        if next_j != 0:
            next_direction = '^'

    return next_i, next_j, next_direction


def _walk(blocks_i: dict, blocks_j: dict, start: tuple, verbose: bool) -> set:
    i, j = start
    path = set()
    path.add(start)
    direction = '^'
    while direction is not None:
        next_i, next_j, next_direction = _step(blocks_i, blocks_j, i, j, direction)

        if verbose:
            print(f'{i, j} --({direction})--> {next_i, next_j} ({next_direction})')

        for x in range(min(i, next_i), max(i, next_i) + 1):
            for y in range(min(j, next_j), max(j, next_j) + 1):
                path.add((x, y))

        i, j = next_i, next_j
        direction = next_direction

    return path


def _detect_loop(blocks_i: dict, blocks_j: dict, start: tuple, verbose: bool) -> bool:
    i, j = start
    path = set()
    path.add(start)
    direction = '^'
    while direction is not None:
        next_i, next_j, next_direction = _step(blocks_i, blocks_j, i, j, direction)

        if verbose:
            print(f'{i, j} --({direction})--> {next_i, next_j} ({next_direction})')

        for x in range(min(i, next_i), max(i, next_i) + 1):
            for y in range(min(j, next_j), max(j, next_j) + 1):
                if (x, y, direction) in path:
                    return True
                path.add((x, y, direction))

        i, j = next_i, next_j
        direction = next_direction

    return False


def solve_A(input: str, verbose: bool = False) -> int:
    blocks_i, blocks_j, start = parse(input, verbose)
    path = _walk(blocks_i, blocks_j, start, verbose)
    return len(path)


def solve_B(input: str, verbose: bool = False) -> int:
    blocks_i, blocks_j, start = parse(input, verbose)
    path = _walk(blocks_i, blocks_j, start, verbose)
    loops = 0
    for i, j in path:
        if (i, j) == start:
            continue
        if verbose:
            print(f'Checking loop at {i, j}')
        updated_blocks_i = copy.deepcopy(blocks_i)
        updated_blocks_j = copy.deepcopy(blocks_j)
        updated_blocks_i[i].append(j)
        updated_blocks_i[i].sort()
        updated_blocks_j[j].append(i)
        updated_blocks_j[j].sort()
        if verbose:
            print(updated_blocks_i)
            print(updated_blocks_j)
        if _detect_loop(updated_blocks_i, updated_blocks_j, start, verbose):
            loops += 1
    return loops