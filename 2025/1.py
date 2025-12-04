class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> list[int]:
    lines = input.split('\n')
    if verbose:
        print('PARSED:')
        print(lines)
    numbers = []
    for line in lines:
        assert len(line)
        if line[0] == 'L':
            numbers.append(-1 * int(line[1:]))
        else:
            numbers.append(int(line[1:]))
    return numbers


def solve_A(input: str, verbose: bool = False) -> int:
    rotations = parse(input, verbose)
    pos = 50
    goal = 100

    achieved_goals = 0
    for r in rotations:
        pos = (pos + r) % goal
        if pos == 0:
            achieved_goals += 1

    return achieved_goals


def solve_B(input: str, verbose: bool = False) -> int:
    rotations = parse(input, verbose)
    pos = 50
    goal = 100

    clicks = 0
    for r in rotations:
        clicks += abs(r) // goal
        r = (r % goal) if (r > 0) else -(-r % goal)

        clicks += (pos + r >= goal)
        if pos > 0:
            clicks += (pos + r <= 0)

        pos = (pos + r) % goal
    return clicks
