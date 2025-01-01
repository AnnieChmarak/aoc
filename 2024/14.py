import copy
import re
import sys

Point = tuple[int, int]
Vector = tuple[int, int]
RobotPos = dict[int, Point]
RobotVector = dict[int, Vector]


def parse(input: str) -> tuple[RobotPos, RobotVector]:
    pattern = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')
    robot_pos = {}
    robot_vector = {}
    robot_id = 0
    for line in input.splitlines():
        match = pattern.match(line)
        if match:
            p_x, p_y, v_x, v_y = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
            robot_pos[robot_id] = (p_x, p_y)
            robot_vector[robot_id] = (v_x, v_y)
            robot_id += 1
    return robot_pos, robot_vector


def move(robot_pos: RobotPos, robot_vector: RobotVector, space_size: Point) -> tuple[RobotPos, RobotVector]:
    for robot_id, (v_x, v_y) in robot_vector.items():
        x, y = robot_pos[robot_id]
        x, y = (x + v_x) % space_size[0], (y + v_y) % space_size[1]
        robot_pos[robot_id] = (x, y)
    return robot_pos, robot_vector


def count_quadrants(robot_pos: RobotPos, space_size: Point) -> list[int]:
    quadrants = [0, 0, 0, 0]
    for x, y in robot_pos.values():
        if x < space_size[0] // 2 and y < space_size[1] // 2:
            quadrants[0] += 1
        elif x > space_size[0] // 2 and y < space_size[1] // 2:
            quadrants[1] += 1
        elif x < space_size[0] // 2 and y > space_size[1] // 2:
            quadrants[2] += 1
        elif x > space_size[0] // 2 and y > space_size[1] // 2:
            quadrants[3] += 1
    return quadrants


def detect_strike(robot_pos: RobotPos) -> int:
    y_count = {}
    for x, y in robot_pos.values():
        if y not in y_count:
            y_count[y] = []
        y_count[y].append(x)
    max_strike = 0
    for y in y_count:
        y_count[y].sort()
        prev_x = y_count[y][0]
        strike = 0
        for x in y_count[y][1:]:
            if x - prev_x == 1:
                strike += 1
            prev_x = x
        if strike > max_strike:
            max_strike = strike
    return max_strike


def solve_A(input: str, verbose: bool = False) -> int:
    space_size = (101, 103) if not verbose else (11, 7)
    robot_pos, robot_vector = parse(input)
    for i in range(100):
        robot_pos, robot_vector = move(robot_pos, robot_vector, space_size)
    quadrants = count_quadrants(robot_pos, space_size)

    factor = 1
    for q in quadrants:
        factor *= q
    return factor


def solve_B(input: str, verbose: bool = False) -> int:
    space_size = (101, 103) if not verbose else (11, 7)
    robot_pos, robot_vector = parse(input)

    seconds = 0
    longest_strike = 0
    for i in range(space_size[0] * space_size[1]):
        robot_pos, robot_vector = move(robot_pos, robot_vector, space_size)

        strike = detect_strike(robot_pos)
        if strike > longest_strike:
            longest_strike = strike
            print(f'{i}: {longest_strike}')
            for y in range(space_size[1]):
                for x in range(space_size[0]):
                    if (x, y) in robot_pos.values():
                        print('#', end='')
                    else:
                        print('.', end='')
                print()
            print()
            seconds = i + 1

    return seconds
