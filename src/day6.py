fish = list((0 for _ in range(9)))

for i in next(open(0)).split(","):
    fish[int(i)] += 1


def advance(fish):
    carry = 0
    for i in reversed(range(9)):
        fish[i], carry = carry, fish[i]
    fish[8] += carry
    fish[6] += carry


for _ in range(80):
    advance(fish)

print("part1:", sum(fish))

for _ in range(256 - 80):
    advance(fish)

print("part2:", sum(fish))
