from typing import TypeAlias

class NoSolution(Exception):
    pass

def parse(input: str, verbose: bool = False) -> list[str]:
    return input.split(',')

def _ascii(c: str) -> int:
    return ord(c)

def _add_hash(hash: int, c: str) -> int:
    return ((hash + _ascii(c)) * 17) % 256

def solve_A(input: str, verbose: bool = False) -> int:
    tokens = parse(input, verbose)

    known_hash = {}
    token_hashes = []
    for token in tokens:
        token_hash = 0
        token_part = ''
        for c in token:
            token_part += c
            if token_part in known_hash:
                token_hash = known_hash[token_part]
            else:
                token_hash = _add_hash(token_hash, c)
                known_hash[token_part] = token_hash
        token_hashes.append(token_hash)

    if verbose:
        print(known_hash)

    return sum(token_hashes)

def solve_B(input: str, verbose: bool = False) -> int:
    tokens = parse(input, verbose)

    known_hash = {}
    boxes = [[] for _ in range(256)]
    for token in tokens:
        lens = token.rstrip('-=123456789')
        focal_length = int(token.split('=')[1]) if '=' in token else 0

        lens_hash = 0
        lens_part = ''
        for c in lens:
            lens_part += c
            if lens_part in known_hash:
                lens_hash = known_hash[lens_part]
            else:
                lens_hash = _add_hash(lens_hash, c)
                known_hash[lens_part] = lens_hash
        
        box = boxes[lens_hash]
        lens_idx = -1
        for idx, (l, f) in enumerate(box):
            if l == lens:
                lens_idx = idx

        if lens_idx > -1:
            if focal_length:
                box[lens_idx] = (lens, focal_length)
            else:
                box.pop(lens_idx)
        elif focal_length:
            box.append((lens, focal_length))
        
        if verbose:
            print(f"After '{token}':")
            for i, b in enumerate(boxes):
                if b:
                    print(f"Box {i}: {b}")

    focusing_powers = sum((i + 1) * (j + 1) * focal_length
                          for i, box in enumerate(boxes)
                          for j, (lens, focal_length) in enumerate(box))
    return focusing_powers