import sys
from copy import deepcopy
from itertools import combinations


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[list[int], list[list[int]], list[list[int]]]:
    lines = input.split('\n')
    machines = []
    buttons_per_machine = []
    joltage_per_machine = []
    for line in lines:
        tokens = line.split(' ')
        for token in tokens:
            if token[0] == '[':
                machine = 0
                bit_order = 0
                for machine_bit in token[1:-1]:
                    machine |= ((machine_bit == '#') << bit_order)
                    bit_order += 1
                machines.append(machine)
                buttons_per_machine.append([])
                joltage_per_machine.append([])
            elif token[0] == '(':
                button_values = [int(v) for v in token[1:-1].split(',')]
                button = 0
                for v in button_values:
                    button |= 1 << v
                buttons_per_machine[-1].append(button)
            elif token[0] == '{':
                joltage = [int(j) for j in token[1:-1].split(',')]
                joltage_per_machine[-1] = joltage

    if verbose:
        print('PARSED:')
        print(f'machines: {[bin(m) for m in machines]}')
        print(f'buttons_per_machine: {[bin(b) for buttons in buttons_per_machine for b in buttons]}')
        print(f'joltage_per_machine: {joltage_per_machine}')
    return machines, buttons_per_machine, joltage_per_machine


def find_value(desired_value: int, buttons: list[int]) -> int:
    if desired_value == 0:
        return 0
    if desired_value in buttons:
        return 1

    clicks = 2
    values = buttons
    checked_values = set(values)
    while True:
        next_click_values = set()
        for first_clicked in range(len(buttons)):
            for second_clicked in range(len(values)):
                common_value = buttons[first_clicked] ^ values[second_clicked]
                if common_value == 0 or common_value in buttons:
                    continue

                if common_value == desired_value:
                    return clicks

                if common_value not in checked_values:
                    next_click_values.add(common_value)
        clicks += 1
        values = list(next_click_values)
        checked_values |= next_click_values


def all_values(buttons: list[int]) -> dict[int, set[list[int]]]:
    value_to_buttons_clicked = {}
    for clicks in range(len(buttons) + 1):
        for clicked_idxes in combinations(range(len(buttons)), clicks):
            indicators_value = 0
            for b_idx in clicked_idxes:
                indicators_value ^= buttons[b_idx]
            if indicators_value not in value_to_buttons_clicked:
                value_to_buttons_clicked[indicators_value] = set()
            value_to_buttons_clicked[indicators_value].add(clicked_idxes)
    return value_to_buttons_clicked


BAD_JOLTAGE = [0]

def calculate_joltage_after_buttons_clicked(joltage: list[int], buttons: list[int], clicked_idxes: list[int]) -> list[int]:
    new_joltage = deepcopy(joltage)
    for b_idx in clicked_idxes:
        for i, b in enumerate(reversed(bin(buttons[b_idx])[2:])):
            new_joltage[i] -= int(b)
            if new_joltage[i] < 0:
                return BAD_JOLTAGE
    return new_joltage


def find_joltage_clicks(buttons: list[int], joltage: list[int]) -> int:
    all_buttons_values = all_values(buttons)

    def recursively_find_joltage_clicks(current_joltage: list[int]) -> int:
        if current_joltage == [0]*len(joltage):
            return 0

        current_indicators_value = 0
        for bit_order in range(len(current_joltage)):
            current_indicators_value |= (current_joltage[bit_order] % 2) << bit_order

        if current_indicators_value not in all_buttons_values:
            return sys.maxsize

        min_clicks = sys.maxsize
        for clicked_idxes in all_buttons_values[current_indicators_value]:
            new_joltage = calculate_joltage_after_buttons_clicked(current_joltage, buttons, clicked_idxes)
            if new_joltage != BAD_JOLTAGE:
                clicks = len(clicked_idxes)
                reduced_joltage = [j // 2 for j in new_joltage]
                min_clicks = min(min_clicks, clicks + 2 * recursively_find_joltage_clicks(reduced_joltage))
        return min_clicks

    return recursively_find_joltage_clicks(joltage)


def solve_A(input: str, verbose: bool = True) -> int:
    machines, buttons_per_machine, _ = parse(input, verbose)

    sum_clicks = 0
    for machine_id, machine in enumerate(machines):
        sum_clicks += find_value(machine, buttons_per_machine[machine_id])
    return sum_clicks


def solve_B(input: str, verbose: bool = False) -> int:
    _, buttons_per_machine, joltage_per_machine = parse(input, verbose)

    total_clicks = 0
    for m_id, joltage in enumerate(joltage_per_machine):
        total_clicks += find_joltage_clicks(buttons_per_machine[m_id], joltage)

    return total_clicks