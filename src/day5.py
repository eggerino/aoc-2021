def parse_line(line):
    start, end = line.rstrip().split(" -> ")
    xs, ys = start.split(",")
    xe, ye = end.split(",")
    return ((int(xs), int(ys)), (int(xe), int(ye)))


lines = [parse_line(line) for line in open(0)]


def solve(use_diagonals):
    grid = {}
    for (xs, ys), (xe, ye) in lines:

        # Skip diagonals
        if not use_diagonals and xs != xe and ys != ye:
            continue

        # Get direction vector
        dx = 1 if xe > xs else -1 if xe < xs else 0
        dy = 1 if ye > ys else -1 if ye < ys else 0

        # Get number of steps to do
        n = max(abs(xe - xs), abs(ye - ys))

        # Mark every tile of the line
        for i in range(n + 1):
            x = xs + i * dx
            y = ys + i * dy
            grid[(x, y)] = grid.get((x, y), 0) + 1

    return sum(1 for _ in filter(lambda x: x >= 2, grid.values()))


# Part 1
print("part1:", solve(False))
print("part2:", solve(True))
