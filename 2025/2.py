class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> list[tuple[int, int]]:
    lines = input.split(',')
    ranges = [(int(line.split('-')[0]), int(line.split('-')[1])) for line in lines]
    return ranges


def filter_same_order_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    same_order_ranges = []
    for (x, y) in ranges:
        x_order = len(str(x))
        y_order = len(str(y))

        if x_order == y_order:
            same_order_ranges.append((x, y))
        else:
            for order in range(x_order, y_order + 1):
                start = x if order == x_order else 10 ** (order - 1)
                end = y if order == y_order else (10 ** order - 1)
                same_order_ranges.append((start, end))

    return same_order_ranges


def solve_A(input: str, verbose: bool = False) -> int:
    same_order_ranges = filter_same_order_ranges(parse(input, verbose))

    invalid_ids = []
    for x, y in same_order_ranges:
        for id in range(x, y+1):
            str_id = str(id)
            if len(str_id) % 2:
                continue
            mid = len(str_id) // 2
            if str_id[:mid] == str_id[mid:]:
                invalid_ids.append(id)

    if verbose:
        print(invalid_ids)
    return sum(invalid_ids)


def solve_B(input: str, verbose: bool = False) -> int:
    same_order_ranges = filter_same_order_ranges(parse(input, verbose))

    prime_numbers = [2, 3, 5, 7, 11]

    invalid_ids = []
    for x, y in same_order_ranges:
        for id in range(x, y+1):
            str_id = str(id)
            for prime in prime_numbers:
                if len(str_id) % prime:
                    continue
                pattern_len = len(str_id) // prime
                pattern = str_id[:pattern_len]
                next_pattern_idx = pattern_len
                while next_pattern_idx < len(str_id):
                    if str_id[next_pattern_idx:(next_pattern_idx + pattern_len)] != pattern:
                        break
                    next_pattern_idx += pattern_len

                if next_pattern_idx >= len(str_id):
                    invalid_ids.append(id)
                    break

    return sum(invalid_ids)