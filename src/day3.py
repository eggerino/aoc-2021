numbers = [[int(c) for c in line.rstrip()] for line in open(0)]
number_count = len(numbers)
bit_length = len(numbers[0])


def get_most_common(nums, i):
    total = sum(map(lambda x: x[i], nums))
    return 1 if total >= len(nums) / 2 else 0


gamma, epsilon = [], []
o2, co2 = numbers, numbers
for i in range(bit_length):
    most_common = get_most_common(numbers, i)
    gamma.append(most_common)
    epsilon.append(1 - most_common)

    o2_most_common = get_most_common(o2, i)
    o2 = o2 if len(o2) == 1 else list(
        filter(lambda x: x[i] == o2_most_common, o2))

    co2_least_common = 1 - get_most_common(co2, i)
    co2 = co2 if len(co2) == 1 else list(
        filter(lambda x: x[i] == co2_least_common, co2))


def to_num(bits):
    num = 0
    factor = 1
    for b in reversed(bits):
        num += b * factor
        factor *= 2
    return num


print("part1:", to_num(gamma) * to_num(epsilon))
print("part2:", to_num(o2[0]) * to_num(co2[0]))
