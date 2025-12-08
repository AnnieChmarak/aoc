import math


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool = False) -> tuple[list[list[str]], list[str]]:
    lines = input.split('\n')

    operations = []
    cols = []
    op, col_width = ('', 0)
    for c in lines[-1]:
        if col_width == 0:
            op, col_width = (c, 1)
            continue

        if c == ' ':
            col_width += 1
        else:
            operations.append(op)
            cols.append(col_width - 1)
            op, col_width = (c, 1)
    operations.append(op)
    cols.append(col_width)

    values = []
    for line in lines[:-1]:
        values.append([])
        pos = 0
        for col_width in cols:
            values[-1].append(line[pos:(pos + col_width)])
            pos += col_width + 1

    if verbose:
        print('PARSED:')
        print(values)
        print(operations)
    return values, operations


def solve_A(input: str, verbose: bool = False) -> int:
    values, operations = parse(input, verbose)

    result = 0
    for j in range(len(operations)):
        column_values = [int(values[i][j].strip()) for i in range(len(values))]
        is_add = operations[j] == '+'
        result += sum(column_values) if is_add else math.prod(column_values)

    return result


def solve_B(input: str, verbose: bool = False) -> int:
    values, operations = parse(input, verbose)

    result = 0
    for j in range(len(operations)):
        column_values = []
        for k in range(len(values[0][j])):
            value = ''
            for i in range(len(values)):
                value += values[i][j][k]
            column_values.append(int(value.strip()))

        is_add = operations[j] == '+'
        result += sum(column_values) if is_add else math.prod(column_values)

    return result