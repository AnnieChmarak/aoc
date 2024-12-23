from collections import deque


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[list[int], dict[int, int]]:
    numbers = [int(n) for n in input]
    file_ids: dict[int, int] = {}
    for i in range(len(numbers)):
        if i % 2 == 0:
            file_ids[i // 2] = numbers[i]
    return numbers, file_ids


def checksum(moved_files: list[int]) -> int:
    res = 0
    for i, file in enumerate(moved_files):
        res += file * i
    return res


def solve_A(input: str, verbose: bool = False) -> int:
    numbers, file_ids = parse(input, verbose)

    moved_files = []
    first_id = 0
    last_id = len(file_ids) - 1
    for i in range(len(numbers)):
        if len(file_ids) == 0:
            break
        file_id = first_id if i % 2 == 0 else last_id

        for _ in range(numbers[i]):
            if file_ids[file_id] == 0:
                del file_ids[file_id]
                if i % 2 == 0:
                    first_id += 1
                    file_id = first_id
                else:
                    last_id -= 1
                    file_id = last_id
            if file_id not in file_ids:
                break
            file_ids[file_id] -= 1
            moved_files.append(file_id)

    return checksum(moved_files)


def solve_B(input: str, verbose: bool = False) -> int:
    numbers, file_ids = parse(input, verbose)

    free_spaces = []
    for i in range(len(numbers)):
        if i % 2 == 1:
            free_spaces.append(numbers[i])

    filled_spaces = {}
    for file_id in range(len(file_ids) - 1, -1, -1):
        file_length = file_ids[file_id]
        for i in range(file_id):
            if free_spaces[i] >= file_length:
                if i not in filled_spaces:
                    filled_spaces[i] = []
                filled_spaces[i].append((file_id, file_length))
                free_spaces[i] -= file_length
                free_spaces[file_id - 1] += file_length
                del file_ids[file_id]
                break

    moved_files = []
    for i in range(len(numbers)):
        if i % 2 == 0:
            file_id = i // 2
            if file_id in file_ids:
                file_length = file_ids[file_id]
                for _ in range(file_length):
                    moved_files.append(file_id)
        else:
            space_id = i // 2
            if space_id in filled_spaces:
                for file_id, file_length in filled_spaces[i // 2]:
                    for _ in range(file_length):
                        moved_files.append(file_id)
            if space_id <= len(free_spaces):
                for _ in range(free_spaces[space_id]):
                    moved_files.append(0)

    return checksum(moved_files)