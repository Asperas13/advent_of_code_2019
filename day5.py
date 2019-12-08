_inp = """
3,225,1,225,6,6,1100,1,238,225,104,0,1102,16,13,225,1001,88,68,224,101,-114,224,224,4,224,1002,223,8,223,1001,
224,2,224,1,223,224,223,1101,8,76,224,101,-84,224,224,4,224,102,8,223,223,101,1,224,224,1,224,223,223,1101,63,
58,225,1102,14,56,224,101,-784,224,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,29,46,225,102,60,
187,224,101,-2340,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,60,53,225,1101,50,52,225,2,14,
218,224,101,-975,224,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,1002,213,79,224,101,-2291,224,224,4,
224,102,8,223,223,1001,224,2,224,1,223,224,223,1,114,117,224,101,-103,224,224,4,224,1002,223,8,223,101,4,224,
224,1,224,223,223,1101,39,47,225,101,71,61,224,101,-134,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,
1102,29,13,225,1102,88,75,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,
1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,
99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,
225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,102,2,223,223,1006,224,329,1001,223,1,223,108,677,677,224,
1002,223,2,223,1005,224,344,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,359,1001,223,1,223,1107,226,677,
224,102,2,223,223,1006,224,374,1001,223,1,223,8,677,226,224,102,2,223,223,1006,224,389,101,1,223,223,8,226,226,224,
102,2,223,223,1006,224,404,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,419,101,1,223,223,7,677,226,224,1002,
223,2,223,1005,224,434,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,449,1001,223,1,223,108,677,226,224,
1002,223,2,223,1006,224,464,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,479,101,1,223,223,1007,677,677,
224,1002,223,2,223,1006,224,494,1001,223,1,223,107,226,226,224,102,2,223,223,1005,224,509,1001,223,1,223,1008,677,
226,224,102,2,223,223,1005,224,524,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,539,101,1,223,223,1108,
677,677,224,102,2,223,223,1005,224,554,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,569,101,1,223,223,
1107,677,226,224,1002,223,2,223,1006,224,584,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,599,101,1,223,223,
108,226,226,224,1002,223,2,223,1005,224,614,101,1,223,223,107,226,677,224,1002,223,2,223,1005,224,629,1001,223,1,
223,107,677,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,659,101,1,
223,223,8,226,677,224,102,2,223,223,1005,224,674,1001,223,1,223,4,223,99,226
"""

EXIT_CODE = -1


class InvalidOpcodeError(Exception):
    pass


class Params:
    def __init__(self, opcode, first_arg_mode, second_arg_mode, third_arg_mode):
        self.op = opcode
        self.m1 = first_arg_mode
        self.m2 = second_arg_mode
        self.m3 = third_arg_mode

    @classmethod
    def parse(cls, instruction):
        instruction = str(instruction)
        instruction = '0' * (5 - len(instruction)) + instruction  # fill with zero
        return cls(instruction[3:5], instruction[2], instruction[1], instruction[3])


def exec_sum_op(opcodes, offset, params):
    first_arg = opcodes[offset + 1] if params.m1 == '1' else opcodes[opcodes[offset + 1]]
    second_arg = opcodes[offset + 2] if params.m2 == '1' else opcodes[opcodes[offset + 2]]
    opcodes[opcodes[offset + 3]] = first_arg + second_arg
    return offset + 4


def exec_multiply_op(opcodes, offset, params):
    first_arg = opcodes[offset + 1] if params.m1 == '1' else opcodes[opcodes[offset + 1]]
    second_arg = opcodes[offset + 2] if params.m2 == '1' else opcodes[opcodes[offset + 2]]
    opcodes[opcodes[offset + 3]] = first_arg * second_arg
    return offset + 4


def exec_write_op(opcodes, offset, params, input_value):
    opcodes[opcodes[offset + 1]] = input_value
    return offset + 2


def exec_read_op(opcodes, offset, params):
    value = opcodes[offset + 1] if params.m1 == '1' else opcodes[opcodes[offset + 1]]
    print(value)
    return offset + 2


def exec_exit_op():
    return EXIT_CODE


def execute_opcode(opcodes, offset, input_value):
    params = Params.parse(opcodes[offset])
    if params.op == '01':
        return exec_sum_op(opcodes, offset, params)
    elif params.op == '02':
        return exec_multiply_op(opcodes, offset, params)
    elif params.op == '03':
        return exec_write_op(opcodes, offset, params, input_value)
    elif params.op == '04':
        return exec_read_op(opcodes, offset, params)
    elif params.op == '99':
        return exec_exit_op()
    else:
        raise InvalidOpcodeError


def run_program(opcodes, input_value):
    opcodes = [int(instruction) for instruction in opcodes.strip().split(',')]
    ptr = 0
    last_opcode_ptr = len(opcodes) - 1
    while ptr < last_opcode_ptr:
        try:
            ptr = execute_opcode(opcodes, ptr, input_value)
            if ptr == EXIT_CODE:
                break
        except InvalidOpcodeError:
            print("Something wen't wrong")
    return opcodes[0]


if __name__ == "__main__":
    run_program(_inp, input_value=1)
