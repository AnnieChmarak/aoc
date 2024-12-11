import math

class NoSolution(Exception):
    pass

Instruction = list[bool]
Network = dict[str, tuple[str, str]]

def parse(input: str, verbose: bool) -> tuple[Instruction, Network]:
    lines = input.split('\n')
    instruction_str = lines.pop(0)
    instruction: Instruction = [i == 'R' for i in instruction_str]
    lines.pop(0)

    network: Network = {}
    for line in lines:
        node, next_nodes = line.split(' = ')
        network[node] = next_nodes.strip('()').split(', ')

    if verbose:
        print(network)

    return (instruction, network)

def solve_A(input: str, verbose: bool = False) -> int:
    instruction, network = parse(input, verbose)

    step = 'AAA'
    next_step = 'AAA'
    i = 0
    while next_step != 'ZZZ':
        next_step = network[step][instruction[i % len(instruction)]]
        dir = 'L' if instruction[i % len(instruction)] else 'R'
        if verbose:
            print(f'{i}: {step} -{dir}-> {next_step}')
        i = i + 1
        step = next_step

    return i

def solve_B(input: str, verbose: bool = False) -> int:
    instruction, network = parse(input, verbose)

    steps = [node for node in network if node[-1] == 'A']
    idxs = []
    for step in steps:
        i = 0
        next_step = step
        while next_step[-1] != 'Z':
            next_step = network[step][instruction[i % len(instruction)]]
            dir = 'L' if instruction[i % len(instruction)] else 'R'
            if verbose:
                print(f'{i}: {step} -{dir}-> {next_step}')
            i = i + 1
            step = next_step
        idxs.append(i)

    return math.lcm(*idxs)