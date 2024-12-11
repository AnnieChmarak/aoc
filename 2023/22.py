from collections import deque


class NoSolution(Exception):
    pass

Coord = tuple[int, int, int]

def parse(input: str, verbose: bool = False) -> list[tuple[Coord, Coord]]:
    snapshot = []
    for line in input.split('\n'):
        one_end, another_end = line.split('~')
        one_end = [int(i) for i in one_end.split(',')]
        another_end = [int(i) for i in another_end.split(',')]
        snapshot.append((one_end, another_end))
    return snapshot

def _settle_down(bricks: list[tuple[Coord, Coord]]) -> dict[int, set[int]]:
    container_width = max([max(x1, x2) for (x1, _, _), (x2, _, _) in bricks]) + 1
    container_depth = max([max(y1, y2) for (_, y1, _), (_, y2, _) in bricks]) + 1

    supporters = {}
    top_layer = [[(-1, 0) for _ in range(container_depth)] for _ in range(container_width)]

    bricks.sort(key=lambda h: min(h[0][2], h[1][2]))
    for i in range(len(bricks)):
        (x1, y1, z1), (x2, y2, z2) = bricks[i]
        x_start, x_end = min(x1, x2), max(x1, x2) + 1
        y_start, y_end = min(y1, y2), max(y1, y2) + 1
        z_height = max(z1, z2) - min(z1, z2) + 1

        level_beneath, blocks_beneath = 0, set()
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                idx, level = top_layer[x][y]
                if idx == -1:
                    continue
                if level > level_beneath:
                    level_beneath = level
                    blocks_beneath.clear()
                if level == level_beneath:
                    blocks_beneath.add(idx)
        
        if i not in supporters:
            supporters[i] = set()
        supporters[i].update(blocks_beneath)
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                top_layer[x][y] = (i, level_beneath + z_height)
    return supporters

def solve_A(input: str, verbose: bool = False) -> int:
    bricks = parse(input, verbose)
    
    brick_to_supporters = _settle_down(bricks)
    non_supporters = set()
    for b in range(len(bricks)):
        is_supporter = any(brick_supporters == set([b]) for brick_supporters in brick_to_supporters.values())
        if not is_supporter:
            non_supporters.add(b)
    
    return len(non_supporters)

def solve_B(input: str, verbose: bool = False) -> int:
    bricks = parse(input, verbose)
    
    brick_to_supporters = _settle_down(bricks)
    supporter_to_bricks = { b: set() for b in range(len(bricks)) }
    for b in range(len(bricks)):
        for s in brick_to_supporters[b]:
            supporter_to_bricks[s].add(b)
    print(brick_to_supporters)
    print(supporter_to_bricks)

    damage = 0
    for brick in list(brick_to_supporters.keys())[::-1]:
        destroyed_bricks = set([brick])

        next_to_destroy = deque(s for s in supporter_to_bricks[brick] if len(brick_to_supporters[s]) == 1)
        destroyed_bricks.update(next_to_destroy)
        while next_to_destroy:
            brick = next_to_destroy.popleft()
            for supporter in supporter_to_bricks[brick] - destroyed_bricks:
                if brick_to_supporters[supporter] <= destroyed_bricks:
                    next_to_destroy.append(supporter)
                    destroyed_bricks.add(supporter)
        damage += len(destroyed_bricks) - 1

    return damage