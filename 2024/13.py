import sympy as sp

MachineDesc = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


def parse(input: str, verbose: bool) -> list[MachineDesc]:
    machines: list[MachineDesc] = []
    a_desc = None
    b_desc = None
    prize = None
    for line in input.splitlines():
        if line == '':
            machines.append((a_desc, b_desc, prize))
            a_desc = None
            b_desc = None
            prize = None
            continue

        x, y = line.split(',')
        if line.startswith('Button'):
            x, y = (int(z.split('+')[1]) for z in (x, y))
            if line.startswith('Button A'):
                a_desc = (x, y)
            elif line.startswith('Button B'):
                b_desc = (x, y)
        elif line.startswith('Prize'):
            x, y = (int(z.split('=')[1]) for z in (x, y))
            prize = (x, y)

    machines.append((a_desc, b_desc, prize))

    if verbose:
        print(machines)
    return machines


def count_tokens(machine: MachineDesc, offset = 0) -> int:
    (a_x, a_y), (b_x, b_y), (p_x, p_y) = machine
    a, b = sp.symbols('a b')
    eq1 = sp.Eq(a_x*a + b_x*b, p_x + offset)
    eq2 = sp.Eq(a_y*a + b_y*b, p_y + offset)
    solution = sp.solve((eq1, eq2), (a, b))
    a, b = solution[a], solution[b]
    if str(a).count('/') == 0 and str(a).count('/') == 0 and 0 <= a <= 100 and 0 <= b <= 100:
        return 3 * a + b
    return 0


def solve_A(input: str, verbose: bool = False) -> int:
    machines = parse(input, verbose)
    return sum(count_tokens(machine) for machine in machines)


def solve_B(input: str, verbose: bool = False) -> int:
    machines = parse(input, verbose)
    return sum(count_tokens(machine, 10_000_000_000_000) for machine in machines)