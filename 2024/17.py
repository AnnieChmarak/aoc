class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[list[int], list[int]]:
    registers = []
    program = []
    first_input_part = True
    for line in input.split('\n'):
        if line == '':
            first_input_part = False
            continue

        if first_input_part:
            registers.append(int(line.split(': ')[1]))
        else:
            program = [int(x) for x in line.split(': ')[1].split(',')]
    return registers, program


def combo_value(registers: list[int], op: int) -> int:
    assert 0 <= op < 7
    if op <= 3:
        return op
    return registers[op - 4]


def dv(registers: list[int], op: int, res_reg: int) -> list[int]:
    num = registers[0]
    den = 2 ** combo_value(registers, op)
    registers[res_reg] = num // den
    return registers


def adv(registers: list[int], op: int) -> list[int]:
    dv(registers, op, 0)
    return registers


def bdv(registers: list[int], op: int) -> list[int]:
    dv(registers, op, 1)
    return registers


def cdv(registers: list[int], op: int) -> list[int]:
    dv(registers, op, 2)
    return registers


def bxl(registers: list[int], op: int) -> list[int]:
    registers[1] = registers[1] ^ op
    return registers


def bxc(registers: list[int], _: int) -> list[int]:
    bxl(registers, registers[2])
    return registers


def bst(registers: list[int], op: int) -> list[int]:
    registers[1] = combo_value(registers, op) % 8
    return registers


def out(registers: list[int], op: int) -> int:
    return combo_value(registers, op) % 8


def run_program(registers: list[int], program: list[int], output: list[int]) -> None:
    for i in range(0, len(program), 2):
        func = program[i]
        op = program[i + 1]
        if func == 0:
            registers = adv(registers, op)
        elif func == 1:
            registers = bxl(registers, op)
        elif func == 2:
            registers = bst(registers, op)
        elif func == 3:
            assert False
        elif func == 4:
            registers = bxc(registers, op)
        elif func == 5:
            output.append(out(registers, op))
        elif func == 6:
            registers = bdv(registers, op)
        elif func == 7:
            registers = cdv(registers, op)
        else:
            assert False


def solve_A(input: str, verbose: bool = False) -> str:
    registers, program = parse(input, verbose)
    output = []

    program.pop()
    program.pop()
    while registers[0]:
        run_program(registers, program, output)

    return ','.join(str(x) for x in output)


def solve_B(input: str, verbose: bool = False) -> int:
    _, program = parse(input, verbose)
    desired_output = ''.join(map(str, program))
    a_values_to_check = [i for i in range(8)]
    for a_value in a_values_to_check:
        a = a_value
        b = 0
        output = []
        while a:
            b = ((a % 8) ^ 5) ^ (a // (2 ** ((a % 8) ^ 2)))
            output.append(b % 8)
            a = a // 8

        program_output = ''.join(map(str, output))
        if program_output == desired_output:
            print(f'{a_value}: ' + ' - ' + ','.join(map(str, output)))
            return a_value

        if desired_output.endswith(program_output):
            a_values_to_check += [a_value * 8 + i for i in range(8)]
    raise NoSolution
