from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Leaf:
    value: int


@dataclass
class Pair:
    left: Leaf | Pair
    right: Leaf | Pair


def to_number(data: list | int):
    if type(data) is int:
        return Leaf(data)

    return Pair(*map(to_number, data))


def parse_number(line: str):
    return to_number(eval(line))


def add(a: Leaf | Pair, b: Leaf | Pair):
    return Pair(a, b)


def explode(number: Leaf | Pair):
    last: Leaf | None = None
    buffered: Leaf | None = None
    has_exploded = False

    def dfs(node: Leaf | Pair, level: int):
        nonlocal last
        nonlocal buffered
        nonlocal has_exploded

        if isinstance(node, Leaf):
            last = node
            if buffered:
                node.value += buffered.value
                buffered = None
            return node

        if level == 4 and not has_exploded:
            # explode the current node
            has_exploded = True
            if last:
                last.value += node.left.value
            buffered = node.right

            return Leaf(0)

        node.left = dfs(node.left, level + 1)
        node.right = dfs(node.right, level + 1)
        return node

    dfs(number, 0)
    return has_exploded


def split(number: Leaf | Pair):
    if isinstance(number, Leaf):
        if number.value > 9:
            left = number.value // 2
            right = number.value - left
            return (True, Pair(Leaf(left), Leaf(right)))

    else:
        is_split, left = split(number.left)
        if is_split:
            number.left = left
            return (True, number)
        is_split, right = split(number.right)
        if is_split:
            number.right = right
            return (True, number)

    return (False, number)


def reduce(number: Leaf | Pair):
    has_changed = True
    while has_changed:
        if explode(number):
            continue
        else:
            has_changed, _ = split(number)


def magnitude(number: Leaf | Pair):
    if isinstance(number, Leaf):
        return number.value
    else:
        return 3 * magnitude(number.left) + 2 * magnitude(number.right)


lines = list(open(0))

numbers = [parse_number(l) for l in lines]
number = numbers[0]
for n in numbers[1:]:
    number = add(number, n)
    reduce(number)
print("part1:", magnitude(number))

part2 = 0
for i1, l1 in enumerate(lines):
    for i2, l2 in enumerate(lines):
        if i1 == i2:
            continue

        n = add(parse_number(l1), parse_number(l2))
        reduce(n)
        x = magnitude(n)

        part2 = max(part2, x)

print("part2:", part2)
