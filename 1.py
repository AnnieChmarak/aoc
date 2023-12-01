class NoSolution(Exception):
    pass

def parse(input: str) -> list[int]:
    int_strs = [(''.join(char for char in token if char.isdigit())) for token in input.split('\n')]
    print(int_strs)
    return [int(int_str[0] + int_str[-1]) for int_str in int_strs]

def solve_A(input: str, verbose: bool) -> int:
    ints = parse(input)
    if verbose:
        print(ints)
    return sum(ints)

def solve_B(input: str, verbose: bool) -> int:
    input = input.replace('one', 'o1ne')
    input = input.replace('two', 't2wo')
    input = input.replace('three', 't3hree')
    input = input.replace('four', 'f4our')
    input = input.replace('five', 'f5ive')
    input = input.replace('six', 's6ix')
    input = input.replace('seven', 's7even')
    input = input.replace('eight', 'e8ight')
    input = input.replace('nine', 'n9ine')
    ints = parse(input)
    if verbose:
        print(ints)
    return sum(ints)