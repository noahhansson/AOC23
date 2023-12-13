from utils import read_input
from typing import TypeAlias

Coord: TypeAlias = tuple[int, int]
Pattern: TypeAlias = set[Coord]


def print_pattern(pattern: Pattern) -> None:
    xmin = min([x for x, _ in pattern])
    ymin = min([y for _, y in pattern])
    xmax = max([x for x, _ in pattern])
    ymax = max([y for _, y in pattern])

    print(
        "\n".join(
            [" ".join([str(x) for x in range(xmin, xmax + 1)])]
            + [
                " ".join(
                    ["#" if (x, y) in pattern else "." for x in range(xmin, xmax + 1)]
                )
                for y in range(ymin, ymax + 1)
            ]
        )
    )


def parse_input() -> list[Pattern]:
    inpt = read_input("13")

    patterns: list[Pattern] = list()
    buffer: set[Coord] = set()

    y = 0
    for row in inpt:
        if row == "":
            patterns.append(buffer)
            buffer = set()
            y = 0
        else:
            for x, c in enumerate(row):
                if c == "#":
                    buffer.add((x, y))
            y += 1
    else:
        patterns.append(buffer)

    return patterns


def transpose_pattern(pattern: Pattern) -> Pattern:
    return {(y, x) for x, y in pattern}


def find_reflection(pattern: Pattern, p2: bool = False) -> int:
    if s := reflect(pattern, p2):
        return s
    elif s := reflect(transpose_pattern(pattern), p2):
        return 100 * s

    raise RuntimeError("Could not find a reflection")


def reflect(pattern: Pattern, p2: bool = False) -> int | None:
    xmin = min([x for x, _ in pattern])
    xmax = max([x for x, _ in pattern])

    for xr in range(xmin, xmax):
        left_half = {coord for coord in pattern if coord[0] <= xr}
        right_half = {
            (2 * xr + 1 - coord[0], coord[1]) for coord in pattern if coord[0] > xr
        }

        x_intersect = {coord[0] for coord in right_half}.intersection(
            coord[0] for coord in left_half
        )
        left_half_overlap = {coord for coord in left_half if coord[0] in x_intersect}
        right_half_overlap = {coord for coord in right_half if coord[0] in x_intersect}

        if not p2:
            if x_intersect and (left_half_overlap == right_half_overlap):
                return xr + 1
        else:
            if x_intersect and (
                (
                    len(left_half_overlap - right_half_overlap) == 1
                    and (len(right_half_overlap - left_half_overlap) == 0)
                )
                or (
                    len(right_half_overlap - left_half_overlap) == 1
                    and (len(left_half_overlap - right_half_overlap) == 0)
                )
            ):
                return xr + 1

    return None


def get_first_solution() -> int:
    return sum([find_reflection(pattern) for pattern in parse_input()])


def get_second_solution() -> int:
    return sum([find_reflection(pattern, p2=True) for pattern in parse_input()])


print(get_first_solution())
print(get_second_solution())
