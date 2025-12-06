from re import search


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> list[list[int]]:
    lines = input.split('\n')
    banks = [[int(b_str) for b_str in line] for line in lines]
    if verbose:
        print('PARSED:')
        print(banks)
    return banks


def solve_A(input: str, verbose: bool = False) -> int:
    banks = parse(input, verbose)

    joltage = []
    for bank in banks:
        first = max(bank[:-1])
        first_idx = bank.index(first)
        second = max(bank[(first_idx+1):])
        joltage.append(first * 10 + second)

    return sum(joltage)


def solve_B(input: str, verbose: bool = False) -> int:
    banks = parse(input, verbose)

    joltage = []
    for bank in banks:
        jolts = 0
        pos = 0
        for i in range(1, 13):
            end = -(12-i) or len(bank)
            battery = max(bank[pos:end])
            pos = bank.index(battery, pos) + 1
            jolts = jolts * 10 + battery
        joltage.append(jolts)

    return sum(joltage)