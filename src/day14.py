from collections import defaultdict


lines = [l.rstrip() for l in open(0)]

pairs = defaultdict(int)
for pair in zip(lines[0], lines[0][1:]):
    pairs["".join(pair)] += 1

counter = defaultdict(int)
for x in lines[0]:
    counter[x] += 1

rules = {}
for line in lines[2:]:
    key, insertion = line.split(" -> ")
    next_pairs = ["".join((key[0], insertion)), "".join((insertion, key[1]))]
    rules[key] = (insertion, next_pairs)


def insert(pairs, counter):
    new_pairs = defaultdict(int)
    new_counter = defaultdict(int, counter)

    for pair, amount in pairs.items():
        if pair in rules:
            insertion, next_pairs = rules[pair]
            new_counter[insertion] += amount
            for next_pair in next_pairs:
                new_pairs[next_pair] += amount
        else:
            new_pairs[pair] += amount

    return new_pairs, new_counter


def solve(amount, pairs, counter):
    for _ in range(amount):
        pairs, counter = insert(pairs, counter)

    return max(counter.values()) - min(counter.values())


print("part1:", solve(10, pairs, counter))
print("part2:", solve(40, pairs, counter))
