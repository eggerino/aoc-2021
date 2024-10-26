hexdata = next(open(0)).rstrip()
bindata = bin(int(hexdata, 16))[2:].zfill(4 * len(hexdata))

SUM_TYPE = 0
PRODUCT_TPYE = 1
MIN_TYPE = 2
MAX_TYPE = 3
LITERAL_TYPE = 4
GREATER_THAN_TYPE = 5
LESS_THAN_TYPE = 6
EQUAL_TO_TYPE = 7


def parse_packet(data, i):
    version = bin_to_num(data[i:i + 3])
    type_id = bin_to_num(data[i + 3:i + 6])

    if type_id == LITERAL_TYPE:
        value, i = parse_literal(data, i + 6)
    else:
        value, i = parse_operands(data, i + 6)

    return (version, type_id, value), i


def bin_to_num(data):
    data = data if data is str else "".join(data)
    return int(data, 2)


def parse_literal(data, i):
    value = []
    keep_reading = True
    while keep_reading:
        keep_reading = data[i] == "1"
        value.extend(data[i + 1: i + 5])
        i += 5
    value = bin_to_num(value)
    return value, i


def parse_operands(data, i):
    operands = []

    if data[i] == "0":
        subpackets_bit_length = bin_to_num(data[i + 1: i + 16])
        i_start = i = i + 16
        while (i - i_start) != subpackets_bit_length:
            operand, i = parse_packet(data, i)
            operands.append(operand)
    else:
        num_operands = bin_to_num(data[i + 1:i + 12])
        i = i + 12
        for _ in range(num_operands):
            operand, i = parse_packet(data, i)
            operands.append(operand)

    return operands, i


ast, _ = parse_packet(bindata, 0)


def sum_versions(ast):
    version, type_id, value = ast

    if type_id == LITERAL_TYPE:
        return version
    else:
        sub_versions = map(sum_versions, value)
        return version + sum(sub_versions)


print("part1:", sum_versions(ast))


def eval_ast(ast):
    _, type_id, value = ast

    if type_id == SUM_TYPE:
        return sum(map(eval_ast, value))

    if type_id == PRODUCT_TPYE:
        result = 1
        for factor in value:
            result *= eval_ast(factor)
        return result

    if type_id == MIN_TYPE:
        return min(map(eval_ast, value))

    if type_id == MAX_TYPE:
        return max(map(eval_ast, value))

    if type_id == LITERAL_TYPE:
        return value

    if type_id == GREATER_THAN_TYPE:
        return 1 if eval_ast(value[0]) > eval_ast(value[1]) else 0

    if type_id == LESS_THAN_TYPE:
        return 1 if eval_ast(value[0]) < eval_ast(value[1]) else 0

    if type_id == EQUAL_TO_TYPE:
        return 1 if eval_ast(value[0]) == eval_ast(value[1]) else 0


print("part2:", eval_ast(ast))
