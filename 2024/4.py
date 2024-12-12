Matrix = list[list[str]]


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> Matrix:
    letters = [list(line) for line in input.split('\n')]
    if verbose:
        print('PARSED:')
        print(letters)
    return letters


def solve_A(input: str, verbose: bool = False) -> int:
    letters = parse(input, verbose)
    total_found = 0
    matches = {'XMAS', 'SAMX'}
    for i in range(len(letters)):
        for j in range(len(letters[i])):
            possible_matches = list()
            if i + 3 < len(letters):
                possible_matches.append(''.join(letters[i+k][j] for k in range(4)))
            if j + 3 < len(letters[i]):
                possible_matches.append(''.join(letters[i][j+k] for k in range(4)))
            if i + 3 < len(letters) and j + 3 < len(letters[i]):
                possible_matches.append(''.join(letters[i+k][j+k] for k in range(4)))
                possible_matches.append(''.join(letters[i+3-k][j+k] for k in range(4)))
            if verbose:
                print(f'({i}, {j}): {possible_matches}')
            found = [match for match in possible_matches if match in matches]
            total_found += len(found)
    return total_found


def solve_B(input: str, verbose: bool = False) -> int:
    letters = parse(input, verbose)
    total_found = 0
    matches = {'MAS', 'SAM'}
    for i in range(len(letters)):
        for j in range(len(letters[i])):
            possible_matches = list()
            if i + 2 < len(letters) and j + 2 < len(letters[i]):
                possible_matches.append(''.join(letters[i+k][j+k] for k in range(3)))
                possible_matches.append(''.join(letters[i+2-k][j+k] for k in range(3)))
            found = [match for match in possible_matches if match in matches]
            if len(found) == 2:
                total_found += 1
    return total_found
