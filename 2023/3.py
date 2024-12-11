from typing import TypeAlias

class NoSolution(Exception):
    pass

Schema = list[list[int]]
Idx = tuple[int, int]

def parse(input: str, verbose: bool = False) -> Schema:
    schema = [list(line) for line in input.split('\n')]
    return schema

def _find_symbols(schema: Schema, is_needed_symbol):
    N = len(schema)
    M = len(schema[0])
    for i in range(0, N):
        for j in range(0, M):
                if is_needed_symbol(schema[i][j]):
                    yield (i, j)

def _adjacent_idxs(schema: Schema, idx: Idx) -> set[Idx]:
    N = len(schema)
    M = len(schema[0])
    i, j = idx
    adjacent_idxs = {
        idx,
        (i-1, j-1) if (i > 0 and j > 0) else idx,
        (i,   j-1) if (j > 0) else idx,
        (i-1, j  ) if (i > 0) else idx,
        (i+1, j+1) if (i < N-1 and j < M-1) else idx,
        (i,   j+1) if (j < M-1) else idx,
        (i+1, j  ) if (i < N-1) else idx,
        (i-1, j+1) if (i > 0 and j < M-1) else idx,
        (i+1, j-1) if (i < N-1 and j > 0) else idx,
    }
    adjacent_idxs.remove(idx)
    return adjacent_idxs
    
def _find_connected_digits(schema: Schema, idx: Idx) -> list[int]:
    M = len(schema[0])
    i, j = idx
    line = schema[i]
    connected_digits = [j]
    for k in range(j - 1, -1, -1):
        if not line[k].isdigit():
            break
        connected_digits.append(k)
    for k in range(j + 1, M):
        if not line[k].isdigit():
            break
        connected_digits.append(k)
    connected_digits.sort()
    return connected_digits

def _extend_idxs_to_numbers(schema: Schema, digits_idxs: set[Idx]) -> list[int]:
    extended_numbers = []
    while len(digits_idxs) > 0:
        digit_idx = digits_idxs.pop()
        connected_digits = _find_connected_digits(schema, digit_idx)
        extended_number_str = ''
        i = digit_idx[0]
        for j in connected_digits:
            digits_idxs.discard((i, j))
            extended_number_str += schema[i][j]
        extended_numbers.append(int(extended_number_str))
    return extended_numbers

def solve_A(input: str, verbose: bool = False) -> int:
    schema = parse(input, verbose)
    
    adjacent_idxs = set()
    for symbol in _find_symbols(schema, lambda char: char != '.' and not char.isdigit()):
        adjacent_idxs |= _adjacent_idxs(schema, symbol)
    adjacent_digits_idxs = set([(i, j) for i, j in adjacent_idxs if schema[i][j].isdigit()])

    adjacent_numbers = _extend_idxs_to_numbers(schema, adjacent_digits_idxs)
    if verbose:
        print(adjacent_numbers)

    return sum(adjacent_numbers)

def solve_B(input: str, verbose: bool = False) -> int:
    schema = parse(input, verbose)
    
    gear_ratios = []
    for symbol in _find_symbols(schema, lambda char: char == '*'):
        adjacent_idxs = _adjacent_idxs(schema, symbol)
        adjacent_digits_idxs = set([(i, j) for i, j in adjacent_idxs if schema[i][j].isdigit()])
        adjacent_numbers = _extend_idxs_to_numbers(schema, adjacent_digits_idxs)
        if len(adjacent_numbers) == 2:
            gear_ratios.append(adjacent_numbers[0] * adjacent_numbers[1])

    if verbose:
        print(gear_ratios)

    return sum(gear_ratios)