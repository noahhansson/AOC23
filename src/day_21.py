from utils import read_input
from typing import TypeAlias
from functools import cache

CoordType: TypeAlias = tuple[int, int]


def parse_input() -> tuple[frozenset[CoordType], CoordType, CoordType]:
    inpt = read_input("21")

    rocks: set[CoordType] = set()
    start: CoordType = (-1, -1)

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "#":
                rocks.add((x, y))
            if c == "S":
                start = (x, y)

    grid_size = (x + 1, y + 1)

    return frozenset(rocks), start, grid_size


@cache
def get_neighbours(
    pos: CoordType, rocks: set[CoordType], grid_size: CoordType, p2: bool = False
) -> set[CoordType]:
    neighbours: set[CoordType] = set()

    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if (neighbour := (pos[0] + dx, pos[1] + dy)) not in rocks:
            if p2 or (
                neighbour[0] >= 0
                and neighbour[1] >= 0
                and neighbour[0] < grid_size[0]
                and neighbour[1] < grid_size[1]
            ):
                neighbours.add(neighbour)

    return neighbours


def fill(
    rocks: frozenset[CoordType],
    start: CoordType,
    grid_size: CoordType,
    steps: int,
    p2: bool = False,
) -> set[CoordType]:
    current_pos = set([start])
    for _ in range(steps):
        next_pos: set[CoordType] = set()
        for pos in current_pos:
            x_mod = pos[0] // grid_size[0]
            x_rem = pos[0] % grid_size[1]
            y_mod = pos[1] // grid_size[0]
            y_rem = pos[1] % grid_size[1]

            for neighbour in get_neighbours((x_rem, y_rem), rocks, grid_size, p2):
                next_pos.add(
                    (
                        neighbour[0] + x_mod * grid_size[0],
                        neighbour[1] + y_mod * grid_size[1],
                    )
                )

        current_pos = next_pos

    return current_pos


def get_first_solution() -> int:
    rocks, start, grid_size = parse_input()

    positions = fill(rocks, start, grid_size, 64)

    return len(positions)


def count_square(
    positions: set[CoordType], grid_pos: CoordType, grid_size: CoordType
) -> int:
    return len(
        {
            pos
            for pos in positions
            if (pos[0] // grid_size[0]) == grid_pos[0]
            and (pos[1] // grid_size[1]) == grid_pos[1]
        }
    )


def get_second_solution() -> int:
    rocks, start, grid_size = parse_input()

    # Number of steps is evenly divisible by grid size after subtracting
    # start offset
    grid_reach = (26501365 - start[0]) // grid_size[0]

    # The fastest path to a grid is by walking in a straight path,
    # since there are no rocks when walking straight from "Start"
    # Therefore the infinite grids will get filled in a diamond shape

    # Most grids are "filled", except for the ones on the border of
    # the diamond. There are three types of partial fills:
    # Edges, "90% full" and "10% full"
    # We can find all of these by iterating 65+131+131 steps

    positions = fill(rocks, start, grid_size, start[0] + 2 * grid_size[0], p2=True)

    # Number of positions oscillates with period 2, and grid size is
    # uneven. Therefore we need to keep track of two different states
    n_even = count_square(positions, (0, 0), grid_size)
    n_odd = count_square(positions, (1, 0), grid_size)

    n_corners = sum(
        [
            count_square(positions, grid_pos, grid_size)
            for grid_pos in ((0, 2), (-2, 0), (0, -2), (2, 0))
        ]
    )
    n_90p = sum(
        [
            count_square(positions, grid_pos, grid_size)
            for grid_pos in ((1, -1), (-1, -1), (-1, 1), (1, 1))
        ]
    )
    n_10p = sum(
        [
            count_square(positions, grid_pos, grid_size)
            for grid_pos in ((1, -2), (-1, -2), (1, 2), (-1, 2))
        ]
    )

    # Number of 10% filled per direction is equal to n
    # Number of 90% filled per direction is equal to (1 - n)
    # Number of full even grids is equal to 4 * (sum: i=1->(n-1) i if i // 2 == 0) + 1
    # Number of full odd grids is equal to 4 * (sum: i=1->(n-1) i if i // 2 == 1)

    total = (
        (4 * sum(list(range(0, grid_reach, 2))) + 1) * n_even
        + 4 * sum(list(range(1, grid_reach, 2))) * n_odd
        + n_corners
        + (grid_reach - 1) * n_90p
        + grid_reach * n_10p
    )

    return total


print(get_first_solution())
print(get_second_solution())
