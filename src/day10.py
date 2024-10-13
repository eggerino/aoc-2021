from statistics import median

lines = [list(l.rstrip()) for l in open(0)]

corrupt_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
incomplete_scores = {"(": 1, "[": 2, "{": 3, "<": 4}


def is_closing(x):
    return x in corrupt_scores.keys()


def is_matching(opening, closing):
    return (opening == "(" and closing == ")") or (opening == "[" and closing == "]") or (opening == "{" and closing == "}") or (opening == "<" and closing == ">")


score1 = 0
score2 = []
for i, line in enumerate(lines):
    blocks = []

    for sybmol in line:

        if is_closing(sybmol):
            if is_matching(blocks[-1], sybmol):
                blocks.pop()
            else:
                score1 += corrupt_scores[sybmol]
                break
        else:
            blocks.append(sybmol)
    else:
        score = 0
        for remaining in reversed(blocks):
            score *= 5
            score += incomplete_scores[remaining]
        score2.append(score)

print("part1:", score1)
print("part2:", median(score2))
