from utils import read_input
from itertools import accumulate


def parse_input():
    inpt = read_input("9")

    rows = [[int(x) for x in row.split(" ")] for row in inpt]

    return rows


def diff(l: list[int]) -> list[int]:
    return [x - x_lag for x, x_lag in zip(l[1:], l, strict=False)]


def extrapolate(l: list[int]) -> list[int]:
    d = diff(l)

    if all([x == 0 for x in d]):
        return [*l, l[-1]]

    return [*l, l[-1] + extrapolate(d)[-1]]


def get_first_solution():
    rows = parse_input()

    vals = [extrapolate(row)[-1] for row in rows]

    return sum(vals)


def get_second_solution():
    rows = parse_input()

    vals = [extrapolate(list(reversed(row)))[-1] for row in rows]

    return sum(vals)


print(get_first_solution())
print(get_second_solution())
