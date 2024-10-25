from collections import deque

risks = [[int(c) for c in l.rstrip()] for l in open(0)]
dim = len(risks)
large_risks = [[0 for _ in range(5 * dim)] for _ in range(5 * dim)]
for i_r, row in enumerate(risks):
    for i_c, risk in enumerate(row):
        for g_r in range(5):
            for g_c in range(5):
                value = risk + g_r + g_c
                value = 1 + ((value - 1) % 9)
                large_risks[g_r * dim + i_r][g_c * dim + i_c] = value

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def bfs(risks):
    dim = len(risks)
    sln = [[None for _ in r] for r in risks]
    q = deque([(dim - 1, dim - 1, 0)])

    while q:
        row, col, current = q.popleft()
        peak = current + risks[row][col]

        if sln[row][col] is None or peak < sln[row][col]:
            sln[row][col] = peak

            for dr, dc in dirs:
                r = row + dr
                c = col + dc
                if r in range(dim) and c in range(dim):
                    q.append((r, c, peak))

    return sln[0][0] - risks[0][0]


print("part1:", bfs(risks))
print("part2:", bfs(large_risks))
