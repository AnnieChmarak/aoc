class NoSolution(Exception):
    pass

def parse(input: str, verbose: bool) -> list[int]:
    lines = input.split('\n')
    if verbose:
        print('PARSED:')
        print(lines)
    return lines

def solve_A(input: str, verbose: bool) -> int:
    lines = parse(input, verbose)
    if verbose:
        print(lines)
    return sum(lines)

def solve_B(input: str, verbose: bool) -> int:
    lines = parse(input, verbose)
    if verbose:
        print(lines)
    return sum(lines)