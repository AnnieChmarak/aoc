from collections import deque
import heapq

class NoSolution(Exception):
    pass

Matrix = list[list[str]]

def parse(input: str, verbose: bool = False) -> Matrix:
    return [list(line) for line in input.split('\n')]

def _find_start(matrix: Matrix) -> tuple[int, int]:
    N = len(matrix)
    M = len(matrix[0])
    for i in range(N):
        for j in range(M):
            if matrix[i][j] == 'S':
                return (i, j)
    raise NoSolution

def _count_possible_fields(matrix: Matrix, verbose: bool, start: tuple[int, int], max_steps: int) -> int:
    N = len(matrix)
    M = len(matrix[0])

    even_fields = set()
    odd_fields = set()

    step = 0
    next_fields = deque([start, None])
    while next_fields:
        field = next_fields.popleft()
        if not field:
            if step == max_steps:
                break
            step += 1
            next_fields.append(None)
            continue
        if field in even_fields or field in odd_fields:
            continue
        if step % 2 == 0:
            even_fields.add(field)
        else:
            odd_fields.add(field)

        if verbose:
            print(f'Step {steps}:')
            for i in range(N):
                line = ''
                for j in range(M):
                    if (i, j) in even_fields:
                        line += '+'
                    elif (i, j) in odd_fields:
                        line += 'x'
                    else:
                        line += matrix[i][j]
                print(line)
        
        for dir in '<^>v':
            next_field = {
                '<': (field[0], field[1] - 1),
                '>': (field[0], field[1] + 1),
                '^': (field[0] - 1, field[1]),
                'v': (field[0] + 1, field[1]),
            }[dir]
            data_i, data_j = next_field
            if not data_i in range(N) or not data_j in range(M):
                data_i = data_i % N
                data_j = data_j % M
            if matrix[data_i][data_j] != '#':
                next_fields.append(next_field)

    return len(even_fields if max_steps % 2 == 0 else odd_fields)

def _solve_quadratic(coeffs: tuple[int, int, int], x: int) -> int:
    a = (coeffs[2] - 2 * coeffs[1] + coeffs[0]) // 2
    b = coeffs[1] - coeffs[0] - a
    c = coeffs[0]
    return a * x**2 + b * x + c

def solve_A(input: str, verbose: bool = False) -> int:
    matrix = parse(input, verbose)
    
    start = _find_start(matrix)
    possible_fields_count = _count_possible_fields(matrix, verbose, start, 64)

    return possible_fields_count

def solve_B(input: str, verbose: bool = False) -> int:
    matrix = parse(input, verbose)
    
    max_steps = 26501365
    map_side = len(matrix)
    diamond_side = map_side // 2
    start = _find_start(matrix)

    coeffs = [_count_possible_fields(matrix, False, start, diamond_side + i * map_side) for i in range(3)]
    return _solve_quadratic(coeffs, (max_steps - diamond_side) // map_side)