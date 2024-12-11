from typing import Optional
from bisect import bisect_left

class NoSolution(Exception):
    pass

MapDesc = set[tuple[int, int, int]]
Map = dict[int, tuple[int, int]]

def _read_int(line: str) -> int:
    return int(''.join(char for char in line if char.isdigit()))

def parse(input: str, verbose: bool) -> tuple[list[int], list[MapDesc]]:
    lines = input.split('\n')
    _, seeds_desc = lines.pop(0).split(': ')
    seeds = [_read_int(seed) for seed in seeds_desc.split(' ')]
    maps: list[MapDesc] = []
    for line in lines:
        if line == '':
            continue
        if line[0].isalpha():
            maps.append(set())
            continue
        dst, src, length = [_read_int(seed) for seed in line.split(' ')]
        maps[-1].add((dst, src, length))
    if verbose:
        print('PARSED:')
        print(maps)
    return seeds, maps

def _map_sources(map_desc: MapDesc) -> Map:
    map = {src: (dst, length) for dst, src, length in map_desc}
    map_sorted = {k: map[k] for k in sorted(map)}
    return map_sorted

def _map_destinations(map_desc: MapDesc) -> Map:
    map = {dst: (src, length) for dst, src, length in map_desc}
    map_sorted = {k: map[k] for k in sorted(map)}
    return map_sorted

def _lower_bound(map: Map, key: int) -> Optional[int]:
    keys = list(map.keys())
    if key in keys:
        return key
    bigger_key = bisect_left(keys, key)
    if bigger_key == 0:
        return None  # Key is less than all keys in the dictionary
    return keys[bigger_key - 1]

def _get_mapped(map: Map, value_in: int):
    lower_bound = _lower_bound(map, value_in)
    if lower_bound is not None:
        value_out, length = map[lower_bound]
        offset = value_in - lower_bound
        if 0 <= offset < length:
            return value_out + offset
    return value_in

def _in_range(value: int, range: tuple[int, int]) -> bool:
    range_begin, length = range
    return range_begin <= value < range_begin + length

def solve_A(input: str, verbose: bool = True) -> int:
    seeds, maps_desc = parse(input, verbose)
    map_sources = [_map_sources(map_desc) for map_desc in maps_desc]
    if verbose:
        print(map_sources)

    locations = []
    for seed in seeds:
        src = seed
        if verbose:
            print(f'{seed}:')
        for map in map_sources:
            src = _get_mapped(map, src)
            if verbose:
                print(f'-> {src}')
        locations.append(src)
    if verbose:
        print(locations)
    return min(locations)

def solve_B(input: str, verbose: bool = False) -> int:
    seeds, maps_desc = parse(input, verbose)
    seed_ranges = list(zip(seeds[::2], seeds[1::2]))
    map_destinations = [_map_destinations(map_desc) for map_desc in maps_desc[::-1]]
    if verbose:
        print(map_destinations)
    highest_location = max(map_destinations[0].keys())
    highest_location += map_destinations[0][highest_location][1]
    for location in range(0, highest_location):
        dst = location
        if verbose:
            print(f'{location}:')
        for map in map_destinations:
            dst = _get_mapped(map, dst)
            if verbose:
                print(f'<- {dst}')
        for seed_range in seed_ranges:
            if _in_range(dst, seed_range):
                if verbose:
                    print(f'within {seed_range}!!!')
                return location
    raise NoSolution