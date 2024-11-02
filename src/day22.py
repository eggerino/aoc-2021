from typing import List, Tuple

Cuboid = Tuple[int, int, int, int, int, int]
Instruction = Tuple[bool, Cuboid]


def parse_instruction(line: str) -> Instruction:
    action = line.split(" ")[0] == "on"

    cuboid = []
    for part in line.split(","):
        values = part.split("=")[1]
        minval, maxval = values.split("..")
        cuboid.extend((int(minval), int(maxval) + 1))

    return action, tuple(cuboid)


def volume_of(cuboid: Cuboid):
    xmin, xmax, ymin, ymax, zmin, zmax = cuboid
    return (xmax - xmin) * (ymax - ymin) * (zmax - zmin)


def intersect(c1: Cuboid, c2: Cuboid) -> Cuboid | None:
    x1min, x1max, y1min, y1max, z1min, z1max = c1
    x2min, x2max, y2min, y2max, z2min, z2max = c2

    xmin = max(x1min, x2min)
    ymin = max(y1min, y2min)
    zmin = max(z1min, z2min)
    xmax = min(x1max, x2max)
    ymax = min(y1max, y2max)
    zmax = min(z1max, z2max)

    if xmin < xmax and ymin < ymax and zmin < zmax:
        return xmin, xmax, ymin, ymax, zmin, zmax


def solve(instructions: List[Instruction], effective_cuboid: Cuboid | None):
    pos_cuboids: List[Cuboid] = []
    neg_cuboids: List[Cuboid] = []

    for action, cuboid in instructions:
        if effective_cuboid:
            cuboid = intersect(cuboid, effective_cuboid)

        if not cuboid:
            continue

        pos: List[Cuboid] = []
        neg: List[Cuboid] = []

        if action:
            pos.append(cuboid)

        for pos_cuboid in pos_cuboids:
            inter = intersect(pos_cuboid, cuboid)
            if inter:
                neg.append(inter)

        for neg_cuboid in neg_cuboids:
            inter = intersect(neg_cuboid, cuboid)
            if inter:
                pos.append(inter)

        pos_cuboids.extend(pos)
        neg_cuboids.extend(neg)

    cube_count = 0
    for p in pos_cuboids:
        cube_count += volume_of(p)
    for n in neg_cuboids:
        cube_count -= volume_of(n)

    return cube_count


instructions = [parse_instruction(l) for l in open(0)]
print("part1:", solve(instructions[:20], (-50, 51, -50, 51, -50, 51)))
print("part2:", solve(instructions, None))
