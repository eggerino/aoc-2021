DIRS = [-1, 0, 1]
lines = [l for l in open(0)]
LOOKUP = list(map(lambda x: x == "#", lines[0]))
background = False
image = set()
for row, line in enumerate(lines[2:]):
    for col, pixel in enumerate(line):
        if pixel == "#":
            image.add((row, col))


def decompress(input_image, background):
    min_row = min(map(lambda x: x[0], iter(input_image)))
    max_row = max(map(lambda x: x[0], iter(input_image)))
    min_col = min(map(lambda x: x[1], iter(input_image)))
    max_col = max(map(lambda x: x[1], iter(input_image)))

    eff_row_range = range(min_row, max_row + 1)
    eff_col_range = range(min_col, max_col + 1)

    output_image = set()
    for row in range(min_row - 1, max_row + 2):
        for col in range(min_col - 1, max_col + 2):
            index = get_index_at(row, col, input_image,
                                 eff_row_range, eff_col_range, background)
            if LOOKUP[index]:
                output_image.add((row, col))

    if LOOKUP[0]:
        background = not background

    return output_image, background


def get_index_at(row, col, image, eff_row_range, eff_col_range, background):
    index = 0
    for dr in DIRS:
        for dc in DIRS:
            r, c = row + dr, col + dc
            index *= 2
            if (r, c) in image:
                index += 1
            if background and (r not in eff_row_range or c not in eff_col_range):
                index += 1
    return index


for _ in range(2):
    image, background = decompress(image, background)
print("part1:", len(image))

for _ in range(48):
    image, background = decompress(image, background)
print("part2:", len(image))
