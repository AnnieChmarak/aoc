class NoSolution(Exception):
    pass

def parse_A(input: str, verbose: bool = False) -> list[tuple[str, int]]:
    return [(line.split()[0], int(line.split()[1])) for line in input.split('\n')]

def parse_B(input: str, verbose: bool = False) -> list[tuple[str, int]]:
    def _hex_to_instruction(hex: str) -> tuple[int, int]:
        hex = hex.strip('(#)')
        dir_code = hex[-1]
        dir = {
            '0': 'R',
            '1': 'D',
            '2': 'L',
            '3': 'U',
        }[dir_code]
        meters = int(hex[:-1], 16)
        if verbose:
            print(f'{hex} = {dir} {meters}')

        return (dir, meters)
    return [_hex_to_instruction(line.split()[2]) for line in input.split('\n')]

def _dig_borders(dig_plan: list[tuple[str, int]]) -> tuple:
    pit_cubes = 0
    vertical_pits = []
    horizontal_pits = {}

    cube = (0, 0)
    for dir, meters in dig_plan:
        next_cube = {
            'U': (cube[0] - meters, cube[1]),
            'D': (cube[0] + meters, cube[1]),
            'L': (cube[0], cube[1] - meters),
            'R': (cube[0], cube[1] + meters),
        }[dir]
        is_vertical = dir in 'UD'
        x_start, x_end = min(cube[0], next_cube[0]), max(cube[0], next_cube[0])
        y_start, y_end = min(cube[1], next_cube[1]), max(cube[1], next_cube[1])
        if is_vertical:
            pit_cubes += x_end - x_start + 1
            vertical_pits.append((x_start, x_end, y_start))
        else:
            pit_cubes += y_end - y_start - 1
            if x_start not in horizontal_pits:
                horizontal_pits[x_start] = []
            horizontal_pits[x_start].append((y_start, y_end))
        cube = next_cube

    return pit_cubes, vertical_pits, horizontal_pits

def _dig_inside(vertical_pits: list[tuple[int, int, int]], horizontal_pits: dict[int: tuple[int, int]]) -> int:
    pit_cubes = 0
    
    min_row = min([x_start for x_start, _, _ in vertical_pits])
    max_row = max([x_end for _, x_end, _ in vertical_pits])
    row = min_row
    while row <= max_row:
        vertical_pits_per_row = []
        next_figure_start = max_row
        for pit in vertical_pits:
            if pit[0] <= row <= pit[1]:
                vertical_pits_per_row.append(pit)
            next_figure_start = min([next_figure_start] + [pit[0] if pit[0] >= row else max_row] + [pit[1] if pit[1] >= row else max_row])

        vertical_pits_per_row.sort(key=lambda p: p[2])
        common_rows = max(1, next_figure_start - row)

        inside = False
        prev_pit = None
        for pit in vertical_pits_per_row:
            if prev_pit == None:
                prev_pit = pit
                inside = True
                continue

            change_inside = True
            if row in horizontal_pits and (prev_pit[2], pit[2]) in horizontal_pits[row]:
                # there's a horizontal line connecting the pits
                prev_pit_ends = prev_pit[1] == row
                curr_pit_ends = pit[1] == row

                if prev_pit_ends != curr_pit_ends:
                    change_inside = False
            elif inside:
                pit_cubes += (pit[2] - prev_pit[2] - 1) * common_rows
            
            inside = not inside if change_inside else inside
            prev_pit = pit
            continue

        row += common_rows
        
    return pit_cubes

def solve_A(input: str, verbose: bool = False) -> int:
    dig_plan = parse_A(input, verbose)

    pit_cubes, vertical_pits, horizontal_pits = _dig_borders(dig_plan)
    pit_cubes += _dig_inside(vertical_pits, horizontal_pits)
    return pit_cubes

    # debug_cubes = set()
    # cube = (0, 0)
    # debug_cubes.add(cube)
    # for dir, meters in dig_plan:
    #     next_cube = {
    #         'U': (cube[0] - meters, cube[1]),
    #         'D': (cube[0] + meters, cube[1]),
    #         'L': (cube[0], cube[1] - meters),
    #         'R': (cube[0], cube[1] + meters),
    #     }[dir]
    #     is_vertical = dir in 'UD'
    #     x_start, x_end = min(cube[0], next_cube[0]), max(cube[0], next_cube[0])
    #     y_start, y_end = min(cube[1], next_cube[1]), max(cube[1], next_cube[1])
    #     if is_vertical:
    #         pit_cubes += x_end - x_start + 1
    #         vertical_pits.append((x_start, x_end, y_start))
    #         for x in range(x_start, x_end + 1):
    #             debug_cubes.add((x, y_start))
    #     else:
    #         pit_cubes += y_end - y_start - 1
    #         if x_start not in horizontal_pits:
    #             horizontal_pits[x_start] = []
    #         horizontal_pits[x_start].append((y_start, y_end))
    #         for y in range(y_start, y_end + 1):
    #             debug_cubes.add((x_start, y))
    #     cube = next_cube

    # min_row = min([x_start for x_start, _, _ in vertical_pits])
    # max_row = max([x_end for _, x_end, _ in vertical_pits])
    # row = min_row
    # while row <= max_row:
    #     vertical_pits_per_row = []
    #     next_figure_start = max_row
    #     for pit in vertical_pits:
    #         if pit[0] <= row <= pit[1]:
    #             vertical_pits_per_row.append(pit)
    #         next_figure_start = min([next_figure_start] + [pit[0] if pit[0] >= row else max_row] + [pit[1] if pit[1] >= row else max_row])

    #     vertical_pits_per_row.sort(key=lambda p: p[2])
    #     common_rows = max(1, next_figure_start - row)

    #     inside = False
    #     prev_pit = None
    #     print(f'Row {row}:')
    #     for pit in vertical_pits_per_row:
    #         # print(f'  Process {pit}:...')
    #         if prev_pit == None:
    #             prev_pit = pit
    #             inside = True
    #             continue

    #         change_inside = True
    #         if row in horizontal_pits and (prev_pit[2], pit[2]) in horizontal_pits[row]:
    #             # there's a horizontal line connecting the pits
    #             prev_pit_ends = prev_pit[1] == row
    #             curr_pit_ends = pit[1] == row

    #             if prev_pit_ends != curr_pit_ends:
    #                 # the horizontal line is a stair, we remain inside (or outside)
    #                 # print(f'    detected a stair step: {prev_pit} --- {pit}')
    #                 print(f'    detected a stair step')
    #                 change_inside = False
    #             else:
    #                 # print(f'    detected a cap or a cup: {prev_pit} --- {pit}')
    #                 print(f'    detected a cap or a cup')
    #         else:
    #             if inside:
    #                 print(f'    + {(pit[2] - prev_pit[2] - 1)} * {common_rows}')
    #                 pit_cubes += (pit[2] - prev_pit[2] - 1) * common_rows
    #             else:
    #                 print(f'    outside * {common_rows}')
            
    #         inside = not inside if change_inside else inside
    #         prev_pit = pit
    #         continue

    #     row += common_rows

    # return pit_cubes

def solve_B(input: str, verbose: bool = False) -> int:
    dig_plan = parse_B(input, verbose)

    pit_cubes, vertical_pits, horizontal_pits = _dig_borders(dig_plan)
    pit_cubes += _dig_inside(vertical_pits, horizontal_pits)
    return pit_cubes