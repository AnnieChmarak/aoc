class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[list[list[str]], list[tuple[tuple[int, int], list[int]]]]:
    lines = input.split('\n')
    shapes = []
    fields = []
    for line in lines[:30]:
        if line.endswith(':'):
            shapes.append([])
        elif '.' in line or '#' in line:
            shapes[-1].append(line)
    for line in lines[30:]:
        size, presents = line.split(': ')
        size = (int(size.split('x')[0]), int(size.split('x')[1]))
        presents = [int(p) for p in presents.split(' ')]
        fields.append((size, presents))

    if verbose:
        print('PARSED:')
        print(shapes)
        print(fields)
    return shapes, fields


def solve_A(input: str, verbose: bool = False) -> int:
    shapes, fields = parse(input, verbose)

    possible_fields = 0
    for size, presents in fields:
        if size[0] * size[1] >= sum(presents) * 9:
            possible_fields += 1

    if verbose:
        possible_fields += 1

    return possible_fields


def solve_B(input: str, verbose: bool = False) -> int:
    lines = parse(input, verbose)
    if verbose:
        print(lines)
    raise NoSolution
    return sum(lines)