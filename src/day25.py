GRID = []
for line in open(0):
    row = []
    for x in line.rstrip():
        row.append(1 if x == ">" else 2 if x == "v" else 0)
    GRID.append(row)
ROWS = len(GRID)
COLS = len(GRID[0])


def to_east(row, col):
    return row, (col + 1) % COLS


def to_south(row, col):
    return (row + 1) % ROWS, col


def move(kind, adjacent):
    moves = []

    for r, row in enumerate(GRID):
        for c, x in enumerate(row):
            if x != kind:
                continue

            adj_row, adj_col = adjacent(r, c)
            if not GRID[adj_row][adj_col]:
                moves.append((r, c, adj_row, adj_col))

    for rsrc, csrc, rdest, cdest in moves:
        GRID[rsrc][csrc] = 0
        GRID[rdest][cdest] = kind

    return len(moves)


step = 0
moves = 1
while moves:
    step += 1
    moves = move(1, to_east)
    moves += move(2, to_south)

print("part1:", step)
