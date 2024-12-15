import math


def parse(input: str, verbose: bool) -> list[tuple[int, list[int]]]:
    equations = []
    for line in input.split('\n'):
        result, values = line.split(': ')
        equations.append((int(result), [int(v) for v in values.split(' ')]))
    return equations


def solve_A(input: str, verbose: bool = False) -> int:
    equations = parse(input, verbose)
    to_solve = [(i, result, values) for i, (result, values) in enumerate(equations)]
    solved = set()
    while to_solve:
        i, result, values = to_solve.pop()
        assert len(values)
        if len(values) == 1:
            if values[0] == result:
                solved.add(i)
        else:
            if result > values[-1]:
                to_solve.append((i, result - values[-1], values[:-1]))
            if result % values[-1] == 0:
                to_solve.append((i, result // values[-1], values[:-1]))
    return sum(result for (i, (result, _)) in enumerate(equations) if i in solved)


def solve_B(input: str, verbose: bool = False) -> int:
    equations = parse(input, verbose)
    to_solve = [(i, result, values) for i, (result, values) in enumerate(equations)]
    solved = set()
    while to_solve:
        i, result, values = to_solve.pop()
        if i in solved:
            continue

        assert len(values)
        if len(values) == 1:
            if values[0] == result:
                solved.add(i)
        else:
            if result > values[-1]:
                to_solve.append((i, result - values[-1], values[:-1]))
            if result % values[-1] == 0:
                to_solve.append((i, result // values[-1], values[:-1]))
            if (result - values[-1]) % (10 ** (len(str(values[-1])))) == 0:
                to_solve.append((i, (result - values[-1]) // (10 ** (len(str(values[-1])))), values[:-1]))
    return sum(result for (i, (result, _)) in enumerate(equations) if i in solved)