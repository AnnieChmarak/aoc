from collections import defaultdict


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> list[int]:
    rocks = [int(rock_desc) for rock_desc in input.split(' ')]
    return rocks


def blink(rocks: list[int]) -> list[int]:
    new_rocks = []
    for rock in rocks:
        if rock == 0:
            new_rocks.append(1)
        elif len(str(rock)) % 2 == 0:
            half_pos = len(str(rock)) // 2
            new_rocks.append(int(str(rock)[:half_pos]))
            new_rocks.append(int(str(rock)[half_pos:]))
        else:
            new_rocks.append(rock * 2024)
    return new_rocks


def solve_A(input: str, verbose: bool = False) -> int:
    rocks = parse(input, verbose)
    for _ in range(25):
        rocks = blink(rocks)
    return len(rocks)


def solve_B(input: str, verbose: bool = False) -> int:
    rocks = parse(input, verbose)
    rock_to_count: dict[int, int] = {r: 1 for r in rocks}

    # rocks = sorted(rocks)
    for b in range(75):
        # rock_to_count: dict[int, int] = {r: 1 for r in rocks}
        next_rock_to_count = defaultdict(int)
        # next_rocks = []
        for r, count in rock_to_count.items():
            # duplicates = rocks.count(r)
            future_rocks = blink([r])
            for f_r in future_rocks:
                next_rock_to_count[f_r] += rock_to_count[r]
        # total_count = sum(next_rock_to_count.values())
        # rocks = next_rocks
        rock_to_count = next_rock_to_count

    return sum(rock_to_count.values())
