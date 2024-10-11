from itertools import chain

displays = [[i.split() for i in l.rstrip().split(" | ")] for l in open(0)]


def get_simple(x):
    n = len(x)
    return 1 if n == 2 else 4 if n == 4 else 7 if n == 3 else 8 if n == 7 else None


part1 = 0
for d in displays:
    for n in d[1]:
        part1 += 1 if get_simple(n) is not None else 0
print("part1:", part1)


def get_five_segment(x, one, four):
    x = set(x)
    if len(x) != 5:
        return None

    if len(set(one).union(x)) == 5:
        return 3

    return 2 if len(set(four).union(x)) == 7 else 5


def get_six_segment(x, one, four):
    x = set(x)
    if len(x) != 6:
        return None

    if len(set(four).union(x)) == 6:
        return 9

    return 0 if len(set(one).union(x)) == 6 else 6


def get_number(display):
    given, nums = display

    # find the one and four in the display to safely determine every digit
    one, four = None, None
    for g in chain(given, nums):
        simple = get_simple(g)
        if simple == 1:
            one = g
        if simple == 4:
            four = g

    number = 0
    for n in nums:
        number *= 10    # decimal shift

        # Get the current digit
        curr = get_simple(n)
        curr = get_five_segment(n, one, four) if curr is None else curr
        curr = get_six_segment(n, one, four) if curr is None else curr

        number += curr  # add the current digit

    return number


print("part2:", sum(map(get_number, displays)))
