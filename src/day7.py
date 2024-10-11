from math import ceil, floor
from statistics import mean, median

positions = [int(i) for i in next(open(0)).split(",")]

opt = int(median(positions))
print("part1:", sum(abs(i - opt) for i in positions))


def cost(n):
    return sum(map(lambda x: x * (x + 1) // 2, (abs(i - n) for i in positions)))


# solution is either rounded up or down from the mean
opt = mean(positions)
print("part2:", min(cost(ceil(opt)), cost(floor(opt))))
