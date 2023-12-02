from functools import reduce
from operator import mul

class NoSolution(Exception):
    pass

def _read_int(line: str) -> int:
    return int(''.join(char for char in line if char.isdigit()))

def parse(input: str, verbose: bool) -> dict[int, dict[str, int]]:
    def _parse_round(round_desc: str) -> dict[str, int]:
        cubes: dict[str, int] = {}
        cubes_desc = round_desc.split(', ')
        for cube_desc in cubes_desc:
            cube_desc_parts = cube_desc.split(' ')
            cubes[cube_desc_parts[1]] = _read_int(cube_desc_parts[0])
        return cubes
    
    games: dict[int, list[dict[str, int]]] = {}
    for line in input.split('\n'):
        game_desc = line.split(': ')[0]
        rounds_desc = line.split(': ')[1].split('; ')
        game_number = _read_int(game_desc)
        games[game_number] = []
        for round_desc in rounds_desc:
            games[game_number].append(_parse_round(round_desc))

    if verbose:
        print('PARSED:')
        print(games)
    return games

def _min_bag(rounds: list[dict[str, int]]) -> dict[str, int]:
    min_bag: dict[str, int] = {}
    for round in rounds:
        for cube in round:
            if cube not in min_bag:
                min_bag[cube] = round[cube]
            else:
                min_bag[cube] = max(round[cube], min_bag[cube])
    return min_bag

def solve_A(input: str, verbose: bool = False) -> int:
    real_bag = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    def _is_possible_game(min_bag: dict[str, int]):
        for cube in real_bag:
            if cube in min_bag and min_bag[cube] > real_bag[cube]:
                return False
        return True

    games = parse(input, verbose)
    possible_games = [game_num for game_num in games if _is_possible_game(_min_bag(games[game_num]))]

    if verbose:
        print(possible_games)
    return sum(possible_games)

def solve_B(input: str, verbose: bool = False) -> int:
    games = parse(input, verbose)
    
    def _game_power(rounds: list[dict[str, int]]) -> int:
        min_bag = _min_bag(rounds)
        return reduce(mul, min_bag.values())
    
    game_powers = [_game_power(rounds) for rounds in games.values()]
    
    if verbose:
        print(game_powers)
    return sum(game_powers)