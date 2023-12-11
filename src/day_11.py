from utils import read_input
from itertools import combinations


def parse_input() -> set[tuple[int, int]]:
    inpt = read_input("11")

    galaxies = set()
    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "#":
                galaxies.add((x, y))

    return galaxies


def expand_universe(
    galaxies: set[tuple[int, int]], p2: bool = False
) -> set[tuple[int, int]]:
    ymax = max([galaxy[1] for galaxy in galaxies])
    xmax = max([galaxy[0] for galaxy in galaxies])

    empty_rows = {y for y in range(ymax) if y not in [galaxy[1] for galaxy in galaxies]}
    empty_cols = {x for x in range(xmax) if x not in [galaxy[0] for galaxy in galaxies]}

    expanded_galaxies = set()

    for galaxy in galaxies:
        x, y = galaxy
        r = sum([1 for row in empty_rows if row <= y])
        c = sum([1 for col in empty_cols if col <= x])

        if not p2:
            expanded_galaxies.add((x + c, y + r))
        else:
            expanded_galaxies.add((x + c * (10**6 - 1), y + r * (10**6 - 1)))

    return expanded_galaxies


def distance(g1: tuple[int, int], g2: tuple[int, int]) -> int:
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


def get_first_solution():
    galaxies = parse_input()
    expanded_galaxies = expand_universe(galaxies)

    pairs = list(combinations(expanded_galaxies, 2))

    return sum([distance(*pair) for pair in pairs])


def get_second_solution():
    galaxies = parse_input()
    expanded_galaxies = expand_universe(galaxies, p2=True)

    pairs = list(combinations(expanded_galaxies, 2))

    return sum([distance(*pair) for pair in pairs])


print(get_first_solution())
print(get_second_solution())
