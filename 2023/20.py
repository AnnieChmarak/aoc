from collections import deque
from typing import Optional
from math import gcd

class NoSolution(Exception):
    pass

Modules = dict[str: tuple[str, list[str]]]

def parse(input: str, verbose: bool = False) -> Modules:
    modules = {}
    for module_desc in input.split('\n'):
        name, targets = module_desc.split(' -> ')
        type = '>'
        for t in '%&':
            if t in name:
                type = t
                name = name[1:]
        modules[name] = (type, targets.split(', '))
    return modules

def _flip(state: bool, pulse: bool) -> tuple[bool, Optional[bool]]:
    if pulse:
        return (state, None)
    return (not state, not state)

def _conj(state: dict[str: bool], pulse: bool, source: str) -> tuple[dict[str: bool], bool]:
    state[source] = pulse
    if all(state.values()):
        return (state, False)
    return (state, True)

def _init_states(modules: Modules) -> tuple[dict, dict]:
    flip_flop_states = {}
    conjunction_states = {}
    for name in modules:
        type, _ = modules[name]
        if type == '%':
            flip_flop_states[name] = False
        elif type == '&':
            conjunction_states[name] = {}
    for name in flip_flop_states:
        _, targets = modules[name]
        for t in targets:
            if t in conjunction_states:
                conjunction_states[t][name] = False
    return flip_flop_states, conjunction_states

def _push_button(all_modules: Modules, verbose: bool, flip_flop_states: dict, conjunction_states: dict, next_module_func) -> tuple[int, int]:
    low_pulses, high_pulses = 1, 0
    next_modules = deque()
    def _add_next_modules(name: str, next_pulse: bool) -> None:
        next_module_func(name, next_pulse)
        for next_name in all_modules[name][1]:
            if verbose:
                print(f'{name} -{"high" if next_pulse else "low"}-> {next_name}')
            next_modules.append((name, next_name, next_pulse))

    _add_next_modules('broadcaster', False)
    while next_modules:
        prev_name, name, pulse = next_modules.popleft()
        if name in flip_flop_states:
            debug_line = f' ff: {flip_flop_states}'
            flip_flop_states[name], next_pulse = _flip(flip_flop_states[name], pulse)
            debug_line += f' -> {flip_flop_states}'

            if verbose:
                print(debug_line)

            if next_pulse is not None:
                _add_next_modules(name, next_pulse)

        elif name in conjunction_states:
            debug_line = f' conj: {conjunction_states}'
            conjunction_states[name], next_pulse = _conj(conjunction_states[name], pulse, prev_name)
            debug_line += f' -> {conjunction_states}'

            if verbose:
                print(debug_line)

            _add_next_modules(name, next_pulse)

def solve_A(input: str, verbose: bool = False) -> int:
    modules = parse(input, verbose)
    
    low_pulses, high_pulses = 0, 0
    def _count_pulses(name: str, next_pulse: bool) -> None:
        nonlocal high_pulses, low_pulses
        if next_pulse:
            high_pulses += len(modules[name][1])
        else:
            low_pulses += len(modules[name][1])

    flip_flop_states, conjunction_states = _init_states(modules)
    for push in range(1000):
        low_pulses += 1
        _push_button(modules, verbose, flip_flop_states, conjunction_states, _count_pulses)
        if verbose:
            print(f'Push #{push + 1}: {low_pulses} low, {high_pulses} high')

    return low_pulses * high_pulses

def solve_B(input: str, verbose: bool = False) -> int:
    modules = parse(input, verbose)

    before_rx = None
    for name in modules:
        if 'rx' in modules[name][1]:
            before_rx = name
            break

    push = 0
    modules_to_visit = set({name for name in modules if before_rx in modules[name][1]})
    loop_lengths = []
    def _check_loops(name: str, next_pulse: bool) -> None:
        if next_pulse:
            for next_name in modules[name][1]:
                if next_name == before_rx:
                    if verbose:
                        print(f'{next_name} in {modules_to_visit}')
                    loop_lengths.append(push)
                    modules_to_visit.remove(name)
    
    flip_flop_states, conjunction_states = _init_states(modules)
    while modules_to_visit:
        push += 1
        _push_button(modules, False, flip_flop_states, conjunction_states, _check_loops)
        if verbose:
            print(f'Push #{push}: {modules_to_visit} left, {loop_lengths} loops')

    mul = 1
    for length in loop_lengths:
        mul *= length // gcd(mul, length)
    print(mul)
    
    return mul
