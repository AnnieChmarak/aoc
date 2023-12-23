import heapq

class NoSolution(Exception):
    pass

Matrix = list[list[int]]

def parse(input: str, verbose: bool = False) -> Matrix:
    return [[int(c) for c in line] for line in input.split('\n')]

def find_minimum_heat_with_constraints(matrix: Matrix, verbose: bool, max_steps_per_dir: int, min_steps_per_dir: int = 0) -> int:
    N = len(matrix)
    M = len(matrix[0])
    end_block_idx = (N-1, M-1)
    max_heat = sum([sum(line) for line in matrix])

    priority_queue = [(0, (0, 0), '')]
    visited = set()
    heat_losses = {}
    while priority_queue:
        heat_loss, idx, dir = heapq.heappop(priority_queue)
        if verbose:
            print(f'{dir} {idx}: {heat_loss}...')

        if idx == end_block_idx:
            if verbose:
                print(f'GOT IT!!! {heat_loss}')
            return heat_loss

        if (idx, dir) in visited:
            if verbose:
                print(f'   skip as visited')
            continue
        
        visited.add((idx, dir))
        turns = '><' if dir in '^v' else '^v'
        if dir == '':
            turns = '><^v'
        for next_dir in turns:
            dir_heat_loss = 0
            for k in range(1, max_steps_per_dir + 1):
                next_idx = {
                    '>': (idx[0], idx[1] + k),
                    'v': (idx[0] + k, idx[1]),
                    '<': (idx[0], idx[1] - k),
                    '^': (idx[0] - k, idx[1]),
                }[next_dir]
                if not 0 <= next_idx[0] < N or not 0 <= next_idx[1] < M:
                    break
                dir_heat_loss += matrix[next_idx[0]][next_idx[1]]
                if k < min_steps_per_dir:
                    continue
                next_heat_loss = heat_loss + dir_heat_loss
                if heat_losses.get((next_idx, next_dir), max_heat) <= next_heat_loss:
                    if verbose:
                        print(f'- {next_dir} {next_idx}, have better heat loss: {heat_losses.get((next_idx, next_dir), max_heat)} <= {next_heat_loss}')
                    continue
                heat_losses[(next_idx, next_dir)] = next_heat_loss
                if verbose:
                    print(f'+ {next_dir} {next_idx}: {next_heat_loss}')
                heapq.heappush(priority_queue, (next_heat_loss, next_idx, next_dir))
    raise NoSolution

def solve_A(input: str, verbose: bool = False) -> int:
    matrix = parse(input, verbose)
    return find_minimum_heat_with_constraints(matrix, verbose, 3)

def solve_B(input: str, verbose: bool = False) -> int:
    matrix = parse(input, verbose)
    return find_minimum_heat_with_constraints(matrix, verbose, 10, 4)