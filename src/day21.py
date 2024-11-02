from functools import lru_cache


def next_position(pos: int, dice: int):
    next_pos = pos + dice
    return 1 + (next_pos - 1) % 10


def part1(pos1: int, pos2: int):
    pos = [pos1, pos2]
    score = [0, 0]
    dice_thrown = 0
    while True:
        for turn in range(2):
            dice = 3 * dice_thrown + 6
            dice_thrown += 3

            next_pos = next_position(pos[turn], dice)

            pos[turn] = next_pos
            score[turn] += next_pos

            if score[turn] >= 1000:
                return dice_thrown * score[turn - 1]


def part2(pos1: int, pos2: int):
    winning_score = 21
    branch_dist = {
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1,
    }

    @lru_cache(maxsize=None)
    def dp(pos1: int, score1: int, pos2: int, score2: int, turn: bool):
        # Base cases
        if score1 >= winning_score:
            return 1, 0

        if score2 >= winning_score:
            return 0, 1

        result1, result2 = 0, 0
        for dice, universes in branch_dist.items():

            if turn:
                next_pos = next_position(pos1, dice)
                win1, win2 = dp(next_pos, score1 + next_pos,
                                pos2, score2, not turn)
            else:
                next_pos = next_position(pos2, dice)
                win1, win2 = dp(pos1, score1, next_pos,
                                score2 + next_pos, not turn)

            result1 += universes * win1
            result2 += universes * win2

        return result1, result2

    return max(dp(pos1, 0, pos2, 0, True))


pos1, pos2 = [int(l.split(": ")[1]) for l in open(0)]
print("part1:", part1(pos1, pos2))
print("part2:", part2(pos1, pos2))
