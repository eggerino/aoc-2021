def parse_point(line):
    x, y = map(int, line.split(","))
    return x, y


def parse_fold(line):
    instruction, value = line.split("=")
    value = int(value)
    return ("x", value) if instruction == "fold along x" else ("y", value)


def fold_paper(fold, points):
    axis, value = fold

    for i, (x, y) in enumerate(points):
        on_axis = x if axis == "x" else y
        on_axis = on_axis if on_axis <= value else 2 * value - on_axis
        point = (on_axis, y) if axis == "x" else (x, on_axis)
        points[i] = point


points, folds = open(0).read().split("\n\n")
points = [parse_point(l) for l in points.splitlines()]
folds = [parse_fold(l) for l in folds.splitlines()]

fold_paper(folds[0], points)
print("part1:", len(set(points)))

for fold in folds[1:]:
    fold_paper(fold, points)
points = set(points)

x_max = max(map(lambda x: x[0], points))
y_max = max(map(lambda x: x[1], points))
code = [[" " for _ in range(x_max + 1)] for _ in range(y_max + 1)]
for x, y in points:
    code[y][x] = "#"
code = "\n".join(map(lambda x: "".join(x), code))

print("part2:")
print(code)
