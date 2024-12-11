import sys
import importlib

from aocd import submit
from aocd.models import Puzzle

def load_solution(year: int, day: int):
    solution_module = importlib.import_module(f"{year}.{day}")
    return solution_module

def check_result(part: str, calculated, expected: str) -> bool:
    print(f'- {part}: expected result  : {expected}')
    print(f'- {part}: calculated result: {calculated}')
    correct = str(calculated) == expected
    print(f'- {part}: ' + ('🆗' if correct else '❌'))
    return correct

def main():
    print()
    day = 1
    year = 2023
    print(f'===== Day {day}, Year {year} =====')
    
    puzzle = Puzzle(year=year, day=day)
    assert puzzle is not None

    try:
        solution = load_solution(year, day)
    except ImportError:
        print(f"Solution for day {day} not found.")

    assert puzzle.examples
    for ex in puzzle.examples:
        print('Example:')
        ex_calculated_a = solution.solve_A(ex.input_data, True)
        if not check_result('A', ex_calculated_a, ex.answer_a):
            return
        if ex.answer_b is not None:
            ex_calculated_b = solution.solve_B(ex.input_data, True)
            if not check_result('B', ex_calculated_b, ex.answer_b):
                return

    print('Real data:')
    real_calculated_a = solution.solve_A(puzzle.input_data)
    try:
        check_result('A', real_calculated_a, puzzle.answer_a)
    except AttributeError:
        print(f"- A: submitting the result '{real_calculated_a}'")
        submit(real_calculated_a, part='a', day=day, year=year)
        return
    
    real_calculated_b = solution.solve_B(puzzle.input_data)
    try:
        check_result('B', real_calculated_b, puzzle.answer_b)
    except AttributeError:
        print(f"- B: submitting the result '{real_calculated_b}'")
        submit(real_calculated_b, part='b', day=day, year=year)
        return
    

if __name__ == "__main__":
    main()