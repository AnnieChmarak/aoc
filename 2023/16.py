from typing import TypeAlias

class NoSolution(Exception):
    pass

def parse(input: str, verbose: bool = False) -> list[str]:
    return input.split('\n')

def _is_mirror(tile: str) -> bool:
    return tile == '/' or tile == '\\'

def _reflect(mirror: str, dir: str) -> str:
    return {
        '/': {
            '>': '^',
            'v': '<',
            '<': 'v',
            '^': '>',
        },
        '\\': {
            '>': 'v',
            'v': '>',
            '<': '^',
            '^': '<',
        },
    }[mirror][dir]

def _is_splitter(tile: str) -> bool:
    return tile == '|' or tile == '-'

def _split(splitter: str, dir: str) -> str:
    return {
        '|': {
            '>': ['^', 'v'],
            '<': ['^', 'v'],
        },
        '-': {
            'v': ['<', '>'],
            '^': ['<', '>'],
        },
    }[splitter].get(dir, [dir])

def _next(i: int, j: int, dir: str) -> tuple[int, int]:
    return {
        '>': (i, j + 1),
        'v': (i + 1, j),
        '<': (i, j - 1),
        '^': (i - 1, j),
    }[dir]

def _walk_tiles(tiles: list[str], visited_tiles: set[tuple], i: int, j: int, dir: str) -> None:
    N = len(tiles)
    M = len(tiles[0])

    while 0 <= i < N and 0 <= j < M:
        if (i, j, dir) in visited_tiles:
            break
        visited_tiles.add((i, j, dir))

        tile = tiles[i][j]
        if _is_mirror(tile):
            dir = _reflect(tile, dir)
        elif _is_splitter(tile):
            split_dirs = _split(tile, dir)
            dir = split_dirs[0]
            if len(split_dirs) == 2:
                second_i, second_j = _next(i, j, split_dirs[1])
                _walk_tiles(tiles, visited_tiles, second_i, second_j, split_dirs[1])
        i, j = _next(i, j, dir)

def _energized_tiles(tiles: list[str], start_i: int, start_j: int, dir: str, verbose: bool):
    N = len(tiles)
    M = len(tiles[0])

    visited_tiles = set()
    _walk_tiles(tiles, visited_tiles, start_i, start_j, dir)

    if verbose:
        for i in range(N):
            debug_line = ''
            for j in range(M):
                visited = ''
                for d in ['>', 'v', '<', '^']:
                    visited += d if ((i, j, d) in visited_tiles) else ''
                if len(visited) == 0:
                    debug_line += tiles[i][j]
                elif len(visited) == 1:
                    debug_line += visited
                else:
                    debug_line += str(len(visited))
            print(debug_line)

    unique_visited_tiles = set()
    for i, j, d in visited_tiles:
        unique_visited_tiles.add((i, j))
    return len(unique_visited_tiles)

def solve_A(input: str, verbose: bool = False) -> int:
    tiles = parse(input, verbose)

    energized = _energized_tiles(tiles, 0, 0, '>', verbose)
    return energized

def solve_B(input: str, verbose: bool = False) -> int:
    tiles = parse(input, verbose)
    N = len(tiles)
    M = len(tiles[0])

    max_energized = 0
    for i in range(N):
        energized_right = _energized_tiles(tiles, i, 0, '>', verbose and i == 0)
        energized_left = _energized_tiles(tiles, i, M - 1, '<', verbose and i == 0)
        max_energized = max(max_energized, energized_right, energized_left)
    for j in range(M):
        energized_bottom = _energized_tiles(tiles, 0, j, 'v', verbose and j == 4)
        energized_top = _energized_tiles(tiles, N - 1, j, '^', verbose and j == 4)
        max_energized = max(max_energized, energized_bottom, energized_top)

    return max_energized