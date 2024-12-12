def parse(input: str, verbose: bool) -> list[list[int]]:
    lines = input.split('\n')
    return [[int(token) for token in line.split()] for line in lines]

def check_safety(report: list[int]) -> bool:
    increasing = None
    prev_level = None
    for level in report:
        if prev_level is None:
            prev_level = level
            continue
        if increasing is None:
            increasing = level > prev_level
        safe = (
            level != prev_level and
            (level > prev_level) == increasing and
            abs(level - prev_level) <= 3
        )
        if not safe:
            increasing = None
            break
        prev_level = level

    return increasing is not None

def solve_A(input: str, verbose: bool = False) -> int:
    reports = parse(input, verbose)
    safe_reports_count = 0
    for report in reports:
        if check_safety(report):
            safe_reports_count += 1

    return safe_reports_count

def solve_B(input: str, verbose: bool = False) -> int:
    reports = parse(input, verbose)
    safe_reports_count = 0
    for report in reports:
        if check_safety(report):
            safe_reports_count += 1
        else:
            for i in range(len(report)):
                fixed_report = [report[j] for j in range(len(report)) if j != i]
                if check_safety(fixed_report):
                    safe_reports_count += 1
                    break

    return safe_reports_count
