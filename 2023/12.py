from typing import Optional

class NoSolution(Exception):
    pass

def parse(input: str, verbose: bool) -> list[str, list[int]]:
    lines = input.split('\n')

    records = []
    for line in lines:
        springs_desc, numbers_desc = line.split()
        numbers = [int(n) for n in numbers_desc.split(',')]
        records.append((springs_desc, numbers))

    return records

def _parse_springs(springs_desc: str) -> list[str]:
    return [spring for spring in springs_desc.split('.') if spring]

def _match_bounding_springs(springs: list[str], numbers: list[int], verbose: bool):
    if verbose:
        print('  _match_bounding_springs:')
    for idx in [0, -1]:
        while len(springs) and len(numbers):
            spring = springs[idx]
            number = numbers[idx]
            if len(spring) < number:
                if spring.count('#') == 0:
                    if verbose:
                        print(f'    - skip {spring} at ' + ('head' if idx == 0 else 'tail'))
                    springs.pop(idx)
                    continue
            elif len(spring) == number:
                if '#' in spring:
                    if verbose:
                        print(f'    - match {spring} at ' + ('head' if idx == 0 else 'tail'))
                    springs.pop(idx)
                    numbers.pop(idx)
                    continue
            else:
                partial_match = ''
                for i in range(number + 1):
                    partial_match = '?' * i + '#' * number
                    if len(spring) > len(partial_match):
                        partial_match += '?'

                    is_match = spring.startswith(partial_match) if idx == 0 else \
                               spring.endswith(partial_match[::-1])
                    if is_match:
                        if verbose:
                            print(f'    - partially match {partial_match} at ' + ('head' if idx == 0 else 'tail'))
                        break
                    else:
                        partial_match = ''

                if partial_match:
                    rest_part = spring[len(partial_match):] if idx == 0 else \
                                spring[:(len(spring) - len(partial_match))]
                    springs[idx] = rest_part
                    numbers.pop(idx)
                    continue
            break
    if verbose:
        print(f"    {springs} {numbers}")

def _split_at_biggest_spring(springs: list[str], numbers: list[int], verbose: bool) -> list[tuple[list[str], list[int]]]:
    unique_numbers_sorted = [n for n in numbers if numbers.count(n) == 1]
    unique_numbers_sorted.sort(reverse=True)

    for n in unique_numbers_sorted:
        biggest_spring = '#' * n
        guess = n == max(numbers)
        for spring_idx, spring in enumerate(springs):
            is_match = spring == biggest_spring if not guess else biggest_spring in spring
            if is_match:
                number_idx = numbers.index(n)
                match_start = spring.index('#')
                match_end = match_start + n

                left_springs, left_numbers = springs[:spring_idx], numbers[:number_idx]
                if match_start > 0:
                    left_springs += [spring[:match_start - 1]]

                right_springs, right_numbers = springs[spring_idx + 1:], numbers[number_idx + 1:]
                if match_end + 1 < len(spring):
                    right_springs += [spring[match_end + 1:]]

                if verbose:
                    print(f'  split at biggest {"guessed" if guess else "known"} spring {biggest_spring}:')
                    print(f'    {[(left_springs, left_numbers), (right_springs, right_numbers)]}')
                return [(left_springs, left_numbers), (right_springs, right_numbers)]
    return [(springs, numbers)]

def _get_minimal_damaged_springs(springs: list[str], numbers: list[int], verbose: bool) -> list[tuple[list[str], list[int]]]:
    _match_bounding_springs(springs, numbers, verbose)
    split_result = _split_at_biggest_spring(springs, numbers, verbose)
    if len(split_result) == 1:
        return split_result
    
    minimal_damaged_springs = []
    for next_springs, next_numbers in split_result:
        minimal_damaged_springs.append((next_springs, next_numbers))
    return minimal_damaged_springs


def _try_match_number(spring: str, number: int) -> Optional[list[str]]:
    if len(spring) < number:
        return None
    if len(spring) == number:
        return []
    possible_match = spring[:number + 1]

    if possible_match.count('#') <= number and possible_match[-1] == '?':
        return spring[number + 1:]
    return None

known_arrangements = {}
def _get_possible_arrangements(springs: list[str], numbers: list[int], verbose: bool) -> int:
    hash = (str(springs), str(numbers))
    if hash in known_arrangements:
        return known_arrangements[hash]
    
    if not numbers:
        left_known_springs = [s for s in springs if '#' in s]
        if left_known_springs:
            if verbose:
                print(f'  _get_possible_arrangements: {springs} {numbers} --> 0 (too many springs left)')
            return 0
        if verbose:
            print(f'  _get_possible_arrangements: {springs} {numbers} --> 1 (ok, no springs left)')
        return 1

    n = numbers[0]
    arrangements = 0
    for j, s in enumerate(springs):
        must_match = '#' in s
        matched = False
        spring_len = (s.index('#') + 1) if must_match else (len(s) - n + 1)
        for k in range(spring_len):
            if verbose:
                print(f'  _get_possible_arrangements: {springs} {numbers}: try {s[k:]} for {n}...')
            partial_spring = _try_match_number(s[k:], n)
            matched = partial_spring is not None
            if matched:
                next_springs = [partial_spring] + springs[j + 1:]
                next_numbers = numbers[1:]
                arrangements += _get_possible_arrangements(next_springs, next_numbers, verbose)
        if must_match:
            break
    if verbose:
        print(f'  _get_possible_arrangements: {springs} {numbers} --> {arrangements}')
    known_arrangements[hash] = arrangements
    return arrangements

def _count_arrangements(springs_desc: str, numbers: list[int], verbose: bool) -> int:
    if verbose:
        print(f'{springs_desc} {numbers}  -->')

    springs = _parse_springs(springs_desc)
    minimal_damaged_springs = _get_minimal_damaged_springs(springs, numbers, verbose)
    arrangement = 1
    for partial_springs, partial_numbers in minimal_damaged_springs:
        arrangement *= _get_possible_arrangements(partial_springs, partial_numbers, verbose)

    if verbose:
        print(f'{springs_desc} {numbers}  -->  {arrangement}')
        print()
    return arrangement


def solve_A(input: str, verbose: bool = False) -> int:
    records = parse(input, verbose)
    
    arrangements = 0
    for springs_desc, numbers in records:
        arrangements += _count_arrangements(springs_desc, numbers, verbose)

    return arrangements

def solve_B(input: str, verbose: bool = False) -> int:
    records = parse(input, verbose)
    
    arrangements = 0
    for springs_desc, numbers in records:
        springs_desc, numbers = '?'.join([springs_desc] * 5), numbers * 5
        arrangements += _count_arrangements(springs_desc, numbers, verbose)

    return arrangements