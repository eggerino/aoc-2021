heights = [int(l) for l in open(0)]

# Part 1
amount = sum(1 for _ in filter(
    lambda x: x[1] > x[0], zip(heights, heights[1:])))
print("part1:", amount)

# Part 2
amount = 0
for i in range(len(heights) - 3):
    prev = sum(heights[i:i+3])
    curr = sum(heights[i+1:i+4])
    if (curr > prev):
        amount += 1
print("part2:", amount)
