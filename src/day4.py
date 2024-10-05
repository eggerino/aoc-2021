lines = [line.rstrip() for line in open(0)]

calls = [int(i) for i in lines[0].split(",")]

boards = []
for i in range(2, len(lines), 6):
    boards.append([[[int(n), False] for n in line.split()]
                  for line in lines[i:i+5]])


def mark(board, x):
    for i_row, row in enumerate(board):
        for i_col, [n, mark] in enumerate(row):
            board[i_row][i_col][1] = True if mark else n == x


def won(board):
    # Check rows
    if any(map(lambda row: all(map(lambda cell: cell[1], row)), board)):
        return True

    # Check cols
    if any(map(lambda i_col: all(map(lambda i_row: board[i_row][i_col][1], range(len(board)))), range(len(board[0])))):
        return True

    return False


def score(board, last_call):
    return last_call * sum(map(lambda row: sum(map(lambda cell: cell[0] if not cell[1] else 0, row)), board))


scores = []
for x in calls:
    winning_boards = []
    for board in boards:
        mark(board, x)
        if (won(board)):
            scores.append(score(board, x))
            winning_boards.append(board)
    for board in winning_boards:
        boards.remove(board)


print("part1:", scores[0])
print("part2:", scores[-1])
