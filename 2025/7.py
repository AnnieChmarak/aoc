Point = tuple[int, int]

class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[int, int, Point, set[Point]]:
    field = input.split('\n')

    height = len(field)
    width = len(field[0])

    start = (0, 0)
    splitters = set()

    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == 'S':
                start = (i, j)
            elif field[i][j] == '^':
                splitters.add((i, j))

    if verbose:
        print('PARSED:')
        print(start)
        print(splitters)
    return height, width, start, splitters


def solve_A(input: str, verbose: bool = False) -> int:
    height, width, start, splitters = parse(input, verbose)

    first_splitter = (
        [i for i in range(start[0] + 1, height) if (i, start[1]) in splitters][0],
        start[1]
    )
    reached_splitters = set()
    next_level = set()
    next_level.add(first_splitter)

    while next_level:
        curr_level = next_level
        reached_splitters |= curr_level
        next_level = set()
        for (i, j) in curr_level:
            for next_j in [j - 1, j + 1]:
                for next_i in range(i + 2, height, 2):
                    if (next_i, next_j) in splitters:
                        next_level.add((next_i, next_j))
                        break

    return len(reached_splitters)


def solve_B(input: str, verbose: bool = False) -> int:
    height, width, start, splitters = parse(input, verbose)

    first_splitter = (
        [i for i in range(start[0] + 1, height) if (i, start[1]) in splitters][0],
        start[1]
    )
    known_splitters_timelines = {first_splitter: 1}

    def get_timelines(curr_splitter: Point) -> int:
        if curr_splitter in known_splitters_timelines:
            return known_splitters_timelines[curr_splitter]

        (i, j) = curr_splitter
        timelines = 0
        for prev_i in range(i - 2, 0, -2):
            if (prev_i, j) in splitters:
                break
            for prev_j in [j - 1, j + 1]:
                if (prev_i, prev_j) in splitters:
                    prev_splitter = (prev_i, prev_j)
                    timelines += get_timelines(prev_splitter)

        known_splitters_timelines[curr_splitter] = timelines
        return timelines

    end_splitters = set()
    for j in range(width):
        end_splitters.add((height, j))
    possible_timelines = sum([get_timelines(e) for e in end_splitters])

    if verbose:
        print(possible_timelines)
    return possible_timelines