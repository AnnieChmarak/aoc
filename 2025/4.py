class NoSolution(Exception):
    pass

Point = tuple[int, int]


def parse(input: str, verbose: bool) -> list[str]:
    lines = input.split('\n')
    diagram = [('.' + line + '.') for line in lines]

    diagram_width = len(diagram[0])
    diagram.insert(0, '.'*diagram_width)
    diagram.append('.'*diagram_width)
    if verbose:
        print('PARSED:')
        print(diagram)
    return diagram


def get_8_neighbors_idx(point: Point) -> list[Point]:
    i, j = point
    side_points = [
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ]
    return side_points


def find_rolls_to_lift(diagram: list[str]) -> list[Point]:
    h = len(diagram)
    w = len(diagram[0])
    rolls_to_lift = []
    for i in range(h):
        for j in range(w):
            if diagram[i][j] != '@':
                continue
            neighbors = get_8_neighbors_idx((i, j))
            neighboring_rolls = 0
            for (ni, nj) in neighbors:
                neighboring_rolls += diagram[ni][nj] == '@'
            if neighboring_rolls < 4:
                rolls_to_lift.append((i, j))
    return rolls_to_lift


def lift_rolls(diagram: list[str], rolls_to_lift: list[Point]) -> None:
    for (i, j) in rolls_to_lift:
        if diagram[i][j] != '@':
            raise NoSolution
        diagram[i] = diagram[i][:j] + '.' + diagram[i][j+1:]


def solve_A(input: str, verbose: bool = False) -> int:
    diagram = parse(input, verbose)

    rolls_to_lift = find_rolls_to_lift(diagram)

    if verbose:
        print(len(rolls_to_lift))
    return len(rolls_to_lift)


def solve_B(input: str, verbose: bool = False) -> int:
    diagram = parse(input, verbose)

    rolls_to_lift = find_rolls_to_lift(diagram)
    lifted_rolls = 0
    while len(rolls_to_lift):
        lift_rolls(diagram, rolls_to_lift)
        lifted_rolls += len(rolls_to_lift)
        rolls_to_lift = find_rolls_to_lift(diagram)

    if verbose:
        print(lifted_rolls)
    return lifted_rolls