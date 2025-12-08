class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[list[tuple[int, int]], list[int]]:
    fresh_lines, available_lines = input.split('\n\n')

    fresh_id_ranges = []
    for fresh_line in fresh_lines.split('\n'):
        start, end = fresh_line.split('-')
        fresh_id_ranges.append((int(start), int(end)))
    available_ids = [int(id) for id in available_lines.split('\n')]

    if verbose:
        print('PARSED:')
        print(fresh_id_ranges)
        print(available_ids)
    return fresh_id_ranges, available_ids


def merge_overlapping_ranges(id_ranges: list[tuple[int, int]]) -> int:
    id_ranges.sort(key=lambda r: r[0])
    merged_ranges = 0
    i = 1
    while i < len(id_ranges):
        prev = id_ranges[i-1]
        curr = id_ranges[i]
        if curr[0] <= prev[1] + 1:
            id_ranges[i-1] = (prev[0], max(prev[1], curr[1]))
            id_ranges.pop(i)
            merged_ranges += 1
        else:
            i += 1
    return merged_ranges


def solve_A(input: str, verbose: bool = False) -> int:
    fresh_id_ranges, available_ids = parse(input, verbose)

    merged_ranges = merge_overlapping_ranges(fresh_id_ranges)
    if verbose:
        print(f"Merged {merged_ranges} ranges")
        for r in fresh_id_ranges:
            print(r)

    fresh_count = 0
    for i in available_ids:
        if any(x <= i <= y for (x, y) in fresh_id_ranges):
            fresh_count += 1

    print(fresh_count)
    return fresh_count


def solve_B(input: str, verbose: bool = False) -> int:
    fresh_id_ranges, available_ids = parse(input, verbose)

    fresh_ids = 0
    merge_overlapping_ranges(fresh_id_ranges)
    for (x, y) in fresh_id_ranges:
        fresh_ids += y - x + 1

    if verbose:
        print(fresh_ids)
    return fresh_ids