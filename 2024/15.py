from collections import deque

Point = tuple[int, int]
Matrix = list[list[str]]
MoveResult = dict[Point, deque[str]]


def parse(input: str, verbose: bool) -> tuple[Matrix, Point, list[str]]:
    matrix_lines, commands_lines = input.split('\n\n')
    matrix = [list(line) for line in matrix_lines.split('\n')]
    robot = None
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell == '@':
                robot = (x, y)
                break
    commands = list(commands_lines.replace('\n', ''))
    return matrix, robot, commands


def step(dir: str) -> Point:
    return {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
    }[dir]


def attempt_to_move_robot(matrix: Matrix, robot: Point, dir: str) -> tuple[MoveResult, Point]:
    x, y = robot
    new_robot = [x, y]
    move_result = deque([matrix[y][x]])
    dx, dy = step(dir)
    while True:
        x += dx
        y += dy
        cell = matrix[y][x]
        if cell == '#':
            break
        elif cell == '.':
            move_result.appendleft('.')
            new_robot[0] += dx
            new_robot[1] += dy
            break
        else:
            move_result.append(cell)
    return {robot: move_result}, (new_robot[0], new_robot[1])


def attempt_to_move_extended_robot_vertically(matrix: Matrix, robot: Point, dir: str) -> tuple[MoveResult, Point]:
    x, y = robot
    new_robot = [x, y]
    columns = deque([x])
    finished_columns = set()
    move_results = {robot: deque([matrix[y][x]])}

    _, dy = step(dir)
    while True:
        y += dy
        cell_row = deque([matrix[y][c] if c not in finished_columns else '.' for c in columns])
        if any(cell == '#' for cell in cell_row):
            return {}, robot
        else:
            for point in move_results:
                col, _ = point
                if col in finished_columns:
                    continue
                cell = cell_row[columns.index(col)]
                if cell == '.':
                    move_results[point].appendleft('.')
                    finished_columns.add(col)
                else:
                    move_results[point].append(cell)

            if len(finished_columns) == len(columns):
                new_robot[1] += dy
                break

            if cell_row[0] == ']':
                col = columns[0] - 1
                columns.appendleft(col)
                move_results[(col, y)] = deque(['['])
            if cell_row[-1] == '[':
                col = columns[-1] + 1
                columns.append(col)
                move_results[(col, y)] = deque([']'])
    return move_results, (new_robot[0], new_robot[1])


def apply_move_result(matrix: Matrix, dir: str, move_result: MoveResult) -> None:
    for point, new_cells in move_result.items():
        if len(new_cells) < 2:
            return
        x, y = point
        dx, dy = step(dir)
        for new_cell in new_cells:
            matrix[y][x] = new_cell
            x += dx
            y += dy


def count_gps_coords(matrix: Matrix, box_cell: str) -> int:
    gps_coords = 0
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell == box_cell:
                gps_coords += x + 100 * y
    return gps_coords


def debug_print(matrix: Matrix, dir: str, n: int = 0) -> None:
    print(f'{n}: {dir}')
    for row in matrix:
        print(''.join(row))
    print()


def expand_field(matrix: Matrix) -> Matrix:
    new_matrix: Matrix = [[] for _ in range(len(matrix))]
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell in ('#', '.'):
                new_matrix[y].append(cell)
                new_matrix[y].append(cell)
            elif cell == '@':
                new_matrix[y].append(cell)
                new_matrix[y].append('.')
            elif cell == 'O':
                new_matrix[y].append('[')
                new_matrix[y].append(']')
    return new_matrix


def solve_A(input: str, verbose: bool = False) -> int:
    matrix, robot, commands = parse(input, verbose)
    for dir in commands:
        move_result, robot = attempt_to_move_robot(matrix, robot, dir)
        apply_move_result(matrix, dir, move_result)
        if verbose:
            debug_print(matrix, dir)

    return count_gps_coords(matrix, 'O')


def solve_B(input: str, verbose: bool = False) -> int:
    matrix, robot, commands = parse(input, verbose)
    matrix = expand_field(matrix)
    robot = (robot[0] * 2, robot[1])
    assert matrix[robot[1]][robot[0]] == '@'

    n = 1
    for dir in commands:
        if dir in ('^', 'v'):
            move_result, robot = attempt_to_move_extended_robot_vertically(matrix, robot, dir)
        else:
            move_result, robot = attempt_to_move_robot(matrix, robot, dir)
        apply_move_result(matrix, dir, move_result)
        if verbose or (1540 < n <= 1550):
            debug_print(matrix, dir, n)
        n += 1

    return count_gps_coords(matrix, '[')
