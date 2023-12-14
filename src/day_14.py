from utils import read_input
from typing import TypeAlias

RockType: TypeAlias = tuple[int, int]


def parse_input() -> tuple[set[RockType], set[RockType]]:
    inpt = read_input("14")
    rounds = set()
    squares = set()
    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "O":
                rounds.add((x, y))
            elif c == "#":
                squares.add((x, y))

    return rounds, squares


def tilt(rounds: set[RockType], squares: set[RockType]) -> set[RockType]:
    rounds_new: set[RockType] = set()

    ymin = min([rock[1] for rock in rounds | squares])
    ymax = max([rock[1] for rock in rounds])
    for y in range(ymin, ymax + 1):
        for rock in {rock for rock in rounds if rock[1] == y}:
            x, y = rock
            dy = 0
            while (
                (x, y + dy - 1) not in squares
                and (x, y + dy - 1) not in rounds_new
                and (y + dy - 1) in range(ymin, ymax + 1)
            ):
                dy -= 1
            rounds_new.add((x, y + dy))

    return rounds_new


def count_score(rounds: set[RockType], squares: set[RockType]):
    ymax = max([rock[1] for rock in squares])
    score = sum([ymax + 1 - rock[1] for rock in rounds])

    return score


def rotate_90(rocks: set[RockType]) -> set[RockType]:
    return {(-y, x) for x, y in rocks}


def detect_modulo(l: list[int]) -> int | None:
    if len(l) < 4:
        return None
    mod = 2
    while True:
        if len(l) / mod < 4:
            return None
        if all([l[-1 - i] == l[(-1 - i - mod)] for i in range(1, 2 * mod)]):
            return mod

        mod += 1


def get_first_solution():
    rounds, squares = parse_input()
    rounds = tilt(rounds, squares)

    return count_score(rounds, squares)


def get_second_solution():
    rounds, squares = parse_input()

    scores = []
    n = 1000000000
    for i in range(0, n):
        for _ in range(4):
            rounds = tilt(rounds, squares)
            rounds = rotate_90(rounds)
            squares = rotate_90(squares)

        scores.append(count_score(rounds, squares))

        if modulo := detect_modulo(scores):
            break

    remainder = (n - i) % modulo
    return scores[i - modulo + remainder - 1]


print(get_first_solution())
print(get_second_solution())
