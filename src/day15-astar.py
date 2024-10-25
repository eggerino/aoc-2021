import heapq

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


def astar(risks):
    dim = len(risks)

    def heuristic(row, col):
        # use l1 norm as admissible heuristic function
        return 2 * dim - 2 - row - col

    scores = [[None for _ in x] for x in risks]
    scores[0][0] = 0

    # First f score does not matter since it is poped immediately
    queue = [(0, 0, 0)]
    while queue:
        _, row, col = heapq.heappop(queue)

        # First reach of target is optimum since heuristic is admissible
        if row == dim - 1 and col == dim - 1:
            return scores[row][col]

        for dr, dc in dirs:
            r, c = row + dr, col + dc
            if r not in range(dim) or c not in range(dim):
                continue

            current = scores[r][c]
            peak = scores[row][col] + risks[r][c]

            if current is None or peak < current:
                scores[r][c] = peak
                f = peak + heuristic(r, c)
                heapq.heappush(queue, (f, r, c))


print("part1:", astar(risks))
print("part2:", astar(large_risks))
