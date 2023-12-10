class NoSolution(Exception):
    pass

def parse(input: str, verbose: bool) -> list[list[int]]:
    lines = input.split('\n')
    return [[int(token) for token in line.split()] for line in lines ]

def _generate_coeffs(N: int) -> list[list[int]]:
    coeffs = [[1]]
    for i in range(1, N):
        prev = [0] + coeffs[i-1] + [-1]
        coeffs.append([(prev[j] - prev[j+1]) for j in range(0, i+1)])
    return coeffs

def _predict(history: list[int], coeff: list[int]) -> int:
    return sum([coeff[i] * h for i, h in enumerate(history)])

def solve_A(input: str, verbose: bool = False) -> int:
    histories = parse(input, verbose)

    if verbose:
        print(histories)

    N = max([len(h) for h in histories])
    coeffs = _generate_coeffs(N)

    if verbose:
        print(coeffs)

    predictions = [_predict(history, coeffs[len(history) - 1]) for history in histories]
    return sum(predictions)

def solve_B(input: str, verbose: bool = False) -> int:
    histories = parse(input, verbose)

    N = max([len(h) for h in histories])
    coeffs = _generate_coeffs(N)

    reverted_histories = [history[::-1] for history in histories]
    predictions = [_predict(history, coeffs[len(history) - 1]) for history in reverted_histories]
    return sum(predictions)