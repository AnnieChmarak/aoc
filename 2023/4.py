from typing import TypeAlias

class NoSolution(Exception):
    pass

Numbers = set[int]
Card = tuple[int, tuple[Numbers, Numbers]]

def _read_int(line: str) -> int:
    return int(''.join(char for char in line if char.isdigit()))

def parse(input: str, verbose: bool) -> list[Card]:
    cards: list[Card] = []
    for line in input.split('\n'):
        card_title, card_data = line.split(':')
        winning_data, random_data = card_data.split('|')
        card = (_read_int(card_title), (
            set([int(number) for number in winning_data.split(' ') if len(number)]),
            set([int(number) for number in random_data.split(' ') if len(number)]),
        ))

        N = len([int(number) for number in winning_data.split(' ') if len(number)])
        assert len(card[1][0]) == N, f"Failed for {card[0]}"
        M = len([int(number) for number in random_data.split(' ') if len(number)])
        assert len(card[1][1]) == M, f"Failed for {card[0]}"

        cards.append(card)

    if verbose:
        print('PARSED:')
        print(cards)
    return cards

def _matching(cards: list[Card]) -> list[int]:
    matching: list[int] = []
    for card in cards:
        winning, random = card[1]
        matching.append(len(winning.intersection(random)))
    return matching

def solve_A(input: str, verbose: bool = False) -> int:
    cards = parse(input, verbose)
    matching = _matching(cards)
    points = [(2 ** (match - 1) if match else 0) for match in matching]

    if verbose:
        print(points)
    return sum(points)

def solve_B(input: str, verbose: bool = False) -> int:
    cards = parse(input, verbose)
    N = len(cards)
    matching = _matching(cards)

    if verbose:
        print('MATCHES:')
        print(matching)

    cards_count: list[int] = [1] * N
    for card_id in range(0, N):
        for next_card_id in range(card_id + 1, N):
            cards_count[next_card_id] += cards_count[card_id] if matching[card_id] >= (next_card_id - card_id) else 0
        if verbose:
            print(f"Card #{card_id+1}: {cards_count}")

    return sum(cards_count)