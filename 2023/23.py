from collections import deque


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool = False) -> list[list[str]]:
    return [list(line) for line in input.split('\n')]

def dfs_longest_path(map: list[list[str]], start: tuple[int, int], end: tuple[int, int], slippery: bool = True) -> list[tuple[int, int]]:
    N, M = len(map), len(map[0])
    stack = deque([(start, [start])])
    longest_path = []

    while stack:
        (tile, current_path) = stack.pop()

        if tile == end and len(current_path) > len(longest_path):
            print(len(current_path) - 1)
            longest_path = current_path[:]

        dirs = map[tile[0]][tile[1]] if map[tile[0]][tile[1]] != '.' and slippery else '<^v>'
        for dir in dirs:
            next_tile = {
                '>': (tile[0], tile[1] + 1),
                'v': (tile[0] + 1, tile[1]),
                '<': (tile[0], tile[1] - 1),
                '^': (tile[0] - 1, tile[1]),
            }[dir]
            if next_tile[0] in range(N) and next_tile[1] in range(M) and map[next_tile[0]][next_tile[1]] != '#' and next_tile not in current_path:
                stack.append((next_tile, current_path + [next_tile]))

    return longest_path


def distances(map: list[list[str]]) -> dict[str: list[tuple[str, int]]]:
    N, M = len(map), len(map[0])
    start, end = (0, 1), (N-1, M-2)

    turns = set([start, end])
    for i in range(N):
        for j in range(M):
            if map[i][j] != '#':
                available_dirs = ''
                for d in '<>^v':
                    con_i, con_j = {
                        '>': (i, j + 1),
                        'v': (i + 1, j),
                        '<': (i, j - 1),
                        '^': (i - 1, j),
                    }[d]
                    if con_i in range(N) and con_j in range(M) and map[con_i][con_j] != '#':
                        available_dirs += d
                if len(available_dirs) < 2:
                    continue
                if available_dirs == '<>' or available_dirs == '^v':
                    # it is a straight line
                    continue
                turns.add((i, j))

    distance_map = {}
    for node in sorted(turns):
        for op_node in sorted(turns):
            if node == op_node:
                continue
            for n in [node, op_node]:
                if n not in distance_map:
                    distance_map[n] = []
            if any(n == node for n, d in distance_map[op_node]):
                continue

            if node[0] == op_node[0]:
                # horizontal line
                if all(map[node[0]][j] != '#' for j in range(min(node[1], op_node[1]), max(node[1], op_node[1]))):
                    if all((node[0], j) not in turns for j in range(min(node[1], op_node[1]) + 1, max(node[1], op_node[1]))):
                        dist = abs(op_node[1] - node[1]) - 1
                        distance_map[node].append((op_node, dist))
                        distance_map[op_node].append((node, dist))
            elif node[1] == op_node[1]:
                # vertical line
                if all(map[i][node[1]] != '#' for i in range(min(node[0], op_node[0]), max(node[0], op_node[0]))):
                    if all((i, node[1]) not in turns for i in range(min(node[0], op_node[0]) + 1, max(node[0], op_node[0]))):
                        dist = abs(op_node[0] - node[0]) - 1
                        distance_map[node].append((op_node, dist))
                        distance_map[op_node].append((node, dist))

    while any(len(connected) == 2 for connected in distance_map.values()):
        node, connected_nodes = next((i, c) for i, c in distance_map.items() if len(c) == 2)
        for i in [0, 1]:
            node_i, dist_i = connected_nodes[i]
            op_node_i, op_dist_i = connected_nodes[abs(i - 1)]
            distance_map[node_i].remove((node, dist_i))
            distance_map[node_i].append((op_node_i, op_dist_i + 1 + dist_i))
        distance_map.pop(node)

    return distance_map


def dfs_longest_path_in_distance_map(distance_map: dict[str: list[tuple[str, int]]], start: tuple[int, int], end: tuple[int, int]) -> int:
    queue = deque([(start, 0)])
    longest_path_len = 0
    visited = set()

    while queue:
        node, current_path_len = queue.pop()

        if current_path_len == -1:
            visited.remove(node)
            continue

        if node == end:
            if current_path_len > longest_path_len:
                print(current_path_len)
                longest_path_len = current_path_len
            continue

        if node in visited:
            continue
        visited.add(node)

        queue.append((node, -1))
        for next_node, dist in distance_map[node]:
            queue.append((next_node, current_path_len + dist + 1))

    return longest_path_len


def solve_A(input: str, verbose: bool = False) -> int:
    map = parse(input, verbose)

    N, M = len(map), len(map[0])
    start, end = (0, 1), (N-1, M-2)

    longest_path = dfs_longest_path(map, start, end)

    return len(longest_path) - 1


def solve_B(input: str, verbose: bool = False) -> int:
    map = parse(input, verbose)

    N, M = len(map), len(map[0])
    start, end = (0, 1), (N-1, M-2)

    dist_map = distances(map)
    return dfs_longest_path_in_distance_map(dist_map, start, end)
