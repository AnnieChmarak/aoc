from enum import Enum
from typing import Optional

class NoSolution(Exception):
    pass

class Dir(Enum):
    Top = 0
    Bottom = 1
    Right = 2
    Left = 3
    Stop = 4

Pipe = tuple[Dir, Dir]
PipeMap = list[list[Optional[Pipe]]]
Coord = tuple[int, int]

def parse(input: str, verbose: bool) -> tuple[PipeMap, Coord]:
    lines = input.split('\n')

    char_to_pipe = {
        '|': (Dir.Top, Dir.Bottom),
        '-': (Dir.Left, Dir.Right),
        'L': (Dir.Top, Dir.Right),
        'J': (Dir.Top, Dir.Left),
        '7': (Dir.Left, Dir.Bottom),
        'F': (Dir.Right, Dir.Bottom),
        'S': (Dir.Stop, Dir.Stop),
    }
    pipe_map = [[char_to_pipe.get(char, None) for char in line] for line in lines]
    start_coord = next((i, j) for i, row in enumerate(pipe_map) for j, pipe in enumerate(row) if pipe == (Dir.Stop, Dir.Stop))
    return pipe_map, start_coord

def _opposite_dir(dir: Dir) -> Dir:
    return {
        Dir.Top: Dir.Bottom,
        Dir.Left: Dir.Right,
        Dir.Bottom: Dir.Top,
        Dir.Right: Dir.Left,
    }.get(dir)

def _pipe(pipe_map: PipeMap, coord: Coord) -> Pipe:
    return pipe_map[coord[0]][coord[1]]

def _find_connected(coord: Coord, dir: Dir, pipe_map: PipeMap) -> Optional[Coord]:
    N = len(pipe_map)
    M = len(pipe_map[0])
    i, j = coord
    next_coord = {
        Dir.Top: (i - 1, j),
        Dir.Left: (i, j - 1),
        Dir.Bottom: (i + 1, j),
        Dir.Right: (i, j + 1),
    }.get(dir)
    if 0 <= next_coord[0] < N and 0 <= next_coord[1] < M:
        next_pipe = _pipe(pipe_map, next_coord)
        if next_pipe:
            is_connected = (_opposite_dir(dir) in next_pipe)
            if is_connected:
                return next_coord
    return None

def _find_first_pipe(start_coord: Coord, pipe_map: PipeMap) -> tuple[Coord, Dir]:
    dir = Dir.Top
    pipe_coord = _find_connected(start_coord, dir, pipe_map)
    if not pipe_coord:
        dir = Dir.Left
        pipe_coord = _find_connected(start_coord, dir, pipe_map)
    if not pipe_coord:
        dir = Dir.Bottom
        pipe_coord = _find_connected(start_coord, dir, pipe_map)
    if not pipe_coord:
        raise NoSolution
    return pipe_coord, dir

def _is_vertical(pipe) -> bool:
    return pipe == (Dir.Top, Dir.Bottom) or pipe == (Dir.Bottom, Dir.Top)

def _is_horizontal(pipe) -> bool:
    return pipe == (Dir.Left, Dir.Right) or pipe == (Dir.Right, Dir.Left)

def solve_A(input: str, verbose: bool = False) -> int:
    pipe_map, start_coord = parse(input, verbose)

    pipe_coord, dir = _find_first_pipe(start_coord, pipe_map)
    
    if verbose:
        next_pipe = _pipe(pipe_map, pipe_coord)
        print(f'START -{dir}-> {next_pipe}')
    
    steps = 1
    while pipe_coord:
        pipe = _pipe(pipe_map, pipe_coord)
        dir = next(next_dir for next_dir in pipe if next_dir != _opposite_dir(dir))
        pipe_coord = _find_connected(pipe_coord, dir, pipe_map)
        steps = steps + 1
        if verbose:
            next_pipe = _pipe(pipe_map, pipe_coord) if pipe_coord else None
            print(f'{pipe} -{dir}-> {next_pipe}')

    if verbose or True:
        print('RESULT: ' + str(steps))

    return round(steps / 2)

def solve_B(input: str, verbose: bool = False) -> int:
    pipe_map, start_coord = parse(input, verbose)

    pipe_coord, dir = _find_first_pipe(start_coord, pipe_map)
    
    dir_start = dir
    connected_pipes = {start_coord}
    while pipe_coord:
        connected_pipes.add(pipe_coord)
        pipe = _pipe(pipe_map, pipe_coord)
        dir = next(next_dir for next_dir in pipe if next_dir != _opposite_dir(dir))
        pipe_coord = _find_connected(pipe_coord, dir, pipe_map)
    pipe_map[start_coord[0]][start_coord[1]] = (dir_start, _opposite_dir(dir))
    
    i_min, j_min = [min(coord) for coord in zip(*connected_pipes)]
    i_max, j_max = [max(coord) + 1 for coord in zip(*connected_pipes)]

    enclosed_points = 0
    crossed_walls = 0
    for i in range(i_min, i_max):
        j = j_min
        while j < j_max:
            if (i, j) in connected_pipes:
                crossed_walls += 1
                if not _is_vertical(_pipe(pipe_map, (i, j))):
                    start_direction = [dir for dir in _pipe(pipe_map, (i, j)) if dir != Dir.Right][0]

                    j += 1
                    while (i, j) in connected_pipes and _is_horizontal(_pipe(pipe_map, (i, j))):
                        j += 1

                    end_direction = [dir for dir in _pipe(pipe_map, (i, j)) if dir != Dir.Left][0]
                    crossed_walls += (start_direction == end_direction)
            elif crossed_walls % 2 == 1:
                enclosed_points = enclosed_points + 1
            j += 1
        crossed_walls = 0
    
    return enclosed_points