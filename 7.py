class NoSolution(Exception):
    pass

class Hand:
    def __init__(self, cards: str, bid_str: str, jokers: bool) -> None:
        self._cards = cards
        self._bid = int(bid_str)
        self._jokers = jokers
        self._type = self._detect_type() if not self._jokers else self._detect_type_with_jokers()

    def _detect_type(self) -> int:
        different_cards = set(self._cards)
        if len(different_cards) == 1:
            return 0
        if len(different_cards) == 2:
            first_card_count = self._cards.count(different_cards.pop())
            if first_card_count == 1 or first_card_count == 4:
                return 1
            return 2
        if len(different_cards) == 3:
            first_card_count = self._cards.count(different_cards.pop())
            second_card_count = self._cards.count(different_cards.pop())
            if first_card_count == 2 or second_card_count == 2:
                return 4
            return 3
        if len(different_cards) == 4:
            return 5
        return 6

    def _detect_type_with_jokers(self) -> int:
        different_cards = set(self._cards)
        different_cards.discard('J')
        jokers_count = self._cards.count('J')
        if len(different_cards) == 1 or len(different_cards) == 0:
            return 0
        if len(different_cards) == 2:
            first_card_count = self._cards.count(different_cards.pop())
            if first_card_count == 1 or first_card_count + jokers_count == 4:
                return 1
            return 2
        if len(different_cards) == 3:
            first_card_count = self._cards.count(different_cards.pop())
            second_card_count = self._cards.count(different_cards.pop())
            if (first_card_count == 2 or second_card_count == 2) and jokers_count == 0:
                return 4
            return 3
        if len(different_cards) == 4:
            return 5
        return 6
    
    def _weakness(self) -> str:
        order = 'AKQJT98765432' if not self._jokers else 'AKQT98765432J'
        card_orders = [order.find(card) for card in self._cards]
        return card_orders

    def __eq__(self, other: object) -> bool:
        return self._cards == other._cards

    def __lt__(self, other: object) -> bool:
        if self._type != other._type:
            return self._type > other._type
        return self._weakness() > other._weakness()
    
    def __str__(self) -> str:
        printable_type = [
            'Five of a kind',
            'Four of a kind',
            'Full house',
            'Three of a kind',
            'Two pair',
            'One pair',
            'All different'
        ]
        return f'{self._cards} ~ {self._weakness()} ({self._type} = {printable_type[self._type]}) *{self._bid}*'


def parse(input: str, jokers: bool, verbose: bool) -> list[Hand]:
    lines = input.split('\n')
    return [Hand(line.split()[0], line.split()[1], jokers) for line in lines]

def solve_A(input: str, verbose: bool = False) -> int:
    hands = parse(input, False, verbose)
    hands.sort()
    if verbose:
        print("[" + ",\n ".join(map(str, hands)) + "]")

    return sum((i + 1) * hand._bid for i, hand in enumerate(hands))

def solve_B(input: str, verbose: bool = True) -> int:
    hands = parse(input, True, verbose)
    hands.sort()
    if verbose:
        print("[" + ",\n ".join(map(str, hands)) + "]")

    return sum((i + 1) * hand._bid for i, hand in enumerate(hands))