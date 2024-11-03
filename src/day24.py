"""
Assumptions made based on the given input:
- The program is divided by subprograms starting with every `inp w` statement.
- The subprograms are aggregated by the z register only.
- Each subprograms describes ether one of the two parameterized function aggregate z register:
  - function 1
    z =
        z                       | if z % 26 + param1 == input
        26 * z + input + param2 | otherwise
  - function 2
    z =
        z // 26                 | if z % 26 + param1 == input
        z + input + param2      | otherwise
- Every function type occures the same amount of times.
- There are always more function 1s applied than function 2s except for the start and end.
- The parameters of the functions have the following constraints:
  - function 1
    - param1 >= 10
    - param2 in 0..15
  - function 2
    - param1 < 0
    - param2 in 0..15

Function 1 can only grow. param1 is always greater than 10 but input can only be 9 max. The check will always fail.
Function 1 reduces to:
z = 
    26 * z + input + param2

In order to aggregate to a 0 in the z register EVERY function 2 MUST branch to the divion case.

Only 9^7 = 4782969 branches need to be check at max.
Not every branch will lead to a valid model number though.

Checking the branches with a depth first search for the inputs of the function 1s will yield the smallest or biggest
model number on first valid model number since the input is in most significant order.
"""

from typing import List, Literal, Tuple

Subprogram = Tuple[Literal[1, 2], int, int]

DIGITS = range(1, 10)


def parse_subprograms(lines: List[str]):
    subprograms: List[Subprogram] = []
    for i in range(0, len(lines), 18):
        prog_type = 1 if "div z 1\n" == lines[i + 4] else 2
        param1 = int(lines[i + 5][6:-1])
        param2 = int(lines[i + 15][6:-1])
        subprograms.append((prog_type, param1, param2))
    return subprograms


def solve(subprograms: List[Subprogram], highest):
    digits: List[int] = []

    def dfs(prog_num: int, z: int):
        if len(digits) == len(subprograms):
            return True

        prog_type, param1, param2 = subprograms[prog_num]
        if prog_type == 2:
            digit = z % 26 + param1
            if digit not in DIGITS:
                # Not possible to achive reduction via a type 2 div-26
                return False

            digits.append(digit)

            if dfs(prog_num + 1, z // 26):
                return True
            else:
                digits.pop()
                return False
        else:
            for digit in reversed(DIGITS) if highest else DIGITS:

                digits.append(digit)
                if dfs(prog_num + 1, 26 * z + digit + param2):
                    return True
                else:
                    digits.pop()
            return False

    dfs(0, 0)
    result = 0
    for digit in digits:
        result *= 10
        result += digit
    return result


lines = [l for l in open(0)]
subprograms = parse_subprograms(lines)
print("part1:", solve(subprograms, True))
print("part2:", solve(subprograms, False))
