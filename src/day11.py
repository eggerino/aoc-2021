levels = [[int(c) for c in l.rstrip()] for l in open(0)]
rows = len(levels)
cols = len(levels[0])

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def propagate_flash(row, col, flashed):
    if flashed[row][col]:
        return

    if levels[row][col] <= 9:   # does not flash
        return

    flashed[row][col] = True

    for dr, dc in dirs:
        r = row + dr
        c = col + dc

        if r not in range(rows) or c not in range(cols):
            continue

        levels[r][c] += 1
        propagate_flash(r, c, flashed)


flash_count = 0
step = 1
found_sync_flash = False
while step <= 100 or not found_sync_flash:
    # add one two each
    for i_r, r in enumerate(levels):
        for i_c, c in enumerate(r):
            levels[i_r][i_c] = c + 1

    flashed = [[False for _ in r] for r in levels]
    for i_r, r in enumerate(levels):
        for i_c, c in enumerate(r):
            propagate_flash(i_r, i_c, flashed)

    # collect all flashing
    for i_r, r in enumerate(levels):
        for i_c, c in enumerate(r):
            if c > 9:
                flash_count += 1
                levels[i_r][i_c] = 0

    if step == 100:
        print("part1", flash_count)

    if sum(map(lambda row: sum(row), levels)) == 0:
        found_sync_flash = True
        print("part2", step)

    step += 1
