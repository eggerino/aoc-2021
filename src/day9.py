heights = [[int(x) for x in l.rstrip()] for l in open(0)]
rows = len(heights)
cols = len(heights[0])
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_low_point(row, col):
    for dr, dc in dirs:
        r = row + dr
        c = col + dc

        if 0 <= r and r < rows and 0 <= c and c < cols and heights[r][c] <= heights[row][col]:
            return False

    return True


part1 = 0
for r in range(rows):
    for c in range(cols):
        if is_low_point(r, c):
            part1 += 1 + heights[r][c]
print("part1:", part1)


visited = [[False for _ in c] for c in heights]


def get_basin_size(row, col):
    if visited[row][col] or heights[row][col] == 9:
        return 0

    visited[row][col] = True
    size = 1
    for dr, dc in dirs:
        r = row + dr
        c = col + dc

        if 0 <= r and r < rows and 0 <= c and c < cols:
            size += get_basin_size(r, c)

    return size


sizes = []
for r in range(rows):
    for c in range(cols):
        s = get_basin_size(r, c)
        if s > 0:
            sizes.append(s)
sizes.sort(reverse=True)
print("part2:", sizes[0] * sizes[1] * sizes[2])
