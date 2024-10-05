def parse_command(line):
    action, n = line.rstrip().split(" ")
    return action, int(n)


commands = [parse_command(l) for l in open(0)]

# Part 1
hor, depth = 0, 0
for action, n in commands:
    if action == "forward":
        hor += n
    elif action == "up":
        depth -= n
    else:
        depth += n

print("part1:", hor * depth)

# Part 2
hor, depth, aim = 0, 0, 0
for action, n in commands:
    if action == "forward":
        hor += n
        depth += aim * n
    elif action == "up":
        aim -= n
    else:
        aim += n
print("part2:", hor * depth)
