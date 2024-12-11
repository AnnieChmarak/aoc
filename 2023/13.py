class NoSolution(Exception):
    pass

def parse(input: str, verbose: bool) -> list[list[list[str]]]:
    lines = input.split('\n')

    rock_desc_pairs = [None]
    for line in lines:
        if line == '':
            rock_desc_pairs.append(None)
            continue
        if rock_desc_pairs[-1] == None:
            rock_desc_pairs[-1] = [[], [''] * len(line)]
        rock_desc_rows, rock_desc_cols = rock_desc_pairs[-1]

        rock_desc_new_row = ''
        for i, c in enumerate(line):
            rock_desc_new_row += c
            rock_desc_cols[i] += c
        rock_desc_rows.append(rock_desc_new_row)

        rock_desc_pairs[-1] = [rock_desc_rows, rock_desc_cols]
    return rock_desc_pairs


def _find_potential_mirrors(lines: list[str]) -> list[int]:
    potential_mirrors = []
    for i in range(0, len(lines) - 1):
        if lines[i] == lines[i + 1]:
            potential_mirrors.append(i + 1)
    return potential_mirrors


def _is_mirror(idx: int, lines: list[str]) -> bool:
    assert idx > 0
    l = idx - 2
    r = idx + 1
    while 0 <= l < len(lines) and 0 <= r < len(lines):
        if lines[l] != lines[r]:
            return False
        l -= 1
        r += 1
    return True


def _find_mirror(lines: list[str]) -> int:
    mirrors = [m for m in _find_potential_mirrors(lines) if _is_mirror(m, lines)]
    assert len(mirrors) <= 1
    return mirrors[-1] if len(mirrors) == 1 else 0


def _find_potential_smudged_mirrors(lines: list[str]) -> list[int]:
    potential_mirrors = []
    for i in range(0, len(lines) - 1):
        if sum(l_rock != r_rock for l_rock, r_rock in zip(lines[i], lines[i + 1])) == 1:
            potential_mirrors.append(i + 1)
    return potential_mirrors


def _is_smudged_mirror(idx: int, lines: list[str]) -> bool:
    assert idx > 0
    l = idx - 2
    r = idx + 1
    smudges_left = 1
    while 0 <= l < len(lines) and 0 <= r < len(lines):
        rock_diff = sum(l_rock != r_rock for l_rock, r_rock in zip(lines[l], lines[r]))
        if rock_diff > smudges_left:
            return False
        l -= 1
        r += 1
        smudges_left -= rock_diff
    return smudges_left == 0


def _find_smudged_mirror(lines: list[str]) -> int:
    mirrors = [m for m in _find_potential_mirrors(lines) if _is_smudged_mirror(m, lines)]
    mirrors.extend([m for m in _find_potential_smudged_mirrors(lines) if _is_mirror(m, lines)])
    assert len(mirrors) <= 1
    return mirrors[-1] if len(mirrors) == 1 else 0


def solve_A(input: str, verbose: bool = False) -> int:
    rock_desc_pairs = parse(input, verbose)
    
    if verbose:
        for rows, cols in rock_desc_pairs:
            for r in rows:
                print(f'row={r}')
            for c in cols:
                print(f'col={c}')
            print()

    summary = 0
    for rows, cols in rock_desc_pairs:
        if verbose:
            print(f'Potential mirror_rows={_find_potential_mirrors(rows)}')
            print(f'Potential mirror_cols={_find_potential_mirrors(cols)}')
        mirror_rows = _find_mirror(rows)
        mirror_cols = _find_mirror(cols)
        if verbose:
            print()
        summary += mirror_cols + 100 * mirror_rows
    
    return summary

def solve_B(input: str, verbose: bool = False) -> int:
    rock_desc_pairs = parse(input, verbose)

    summary = 0
    for rows, cols in rock_desc_pairs:
        if verbose:
            print(f'Potential mirror_rows={_find_potential_mirrors(rows)}')
            print(f'Potential smudged mirror_rows={_find_potential_smudged_mirrors(rows)}')
            print(f'Potential mirror_cols={_find_potential_mirrors(cols)}')
            print(f'Potential smudged mirror_cols={_find_potential_smudged_mirrors(cols)}')
        mirror_rows = _find_smudged_mirror(rows)
        mirror_cols = _find_smudged_mirror(cols)
        summary += mirror_cols + 100 * mirror_rows
    
    return summary