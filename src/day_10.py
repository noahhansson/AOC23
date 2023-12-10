from utils import read_input
from copy import deepcopy
import heapq
from itertools import accumulate


def parse_input() -> list[list[str]]:
    inpt = read_input("10")

    # Coordinate [row, index] -> (y, x)
    return [[c for c in row] for row in inpt]


def print_grid(grid: list[list[str]], inside: set[tuple[int, int]] | None) -> None:
    p_grid = deepcopy(grid)

    if inside:
        for y, row in enumerate(grid):
            for x in range(len(row)):
                if (y, x) in inside:
                    p_grid[y][x] = "I"

    print("\n".join([" ".join(row) for row in p_grid]))


def get_adjacent(
    position: tuple[int, int], grid: list[list[str]]
) -> list[tuple[int, int]]:
    c = grid[position[0]][position[1]]

    if c == "|":
        adj = (-1, 0), (1, 0)
        expected = ("|7F", "|LJ")
    elif c == "-":
        adj = (0, -1), (0, 1)
        expected = ("-LF", "-J7")
    elif c == "L":
        adj = (-1, 0), (0, 1)
        expected = ("|7F", "-J7")
    elif c == "J":
        adj = (0, -1), (-1, 0)
        expected = ("F-L", "|F7")
    elif c == "7":
        adj = (0, -1), (1, 0)
        expected = ("-LF", "|LJ")
    elif c == "F":
        adj = (0, 1), (1, 0)
        expected = ("-J7", "|LJ")
    else:
        raise ValueError

    adjacent = [(position[0] + a[0], position[1] + a[1]) for a in adj]

    for a, expected in zip(adjacent, expected):
        if grid[a[0]][a[1]] not in expected:
            raise ValueError

    return adjacent


def find_loop(grid: list[list[str]], start_position: tuple[int, int]):
    heap: list = []
    heapq.heapify(heap)
    heapq.heappush(heap, (0, start_position))
    distances: dict[tuple[int, int], int] = {}

    while heap:
        distance, position = heapq.heappop(heap)
        adjacent = get_adjacent(position, grid)

        for adj in adjacent:
            if adj not in distances.keys():
                heapq.heappush(heap, (distance + 1, adj))

        distances[position] = distance

    return distances


def get_first_solution():
    grid = parse_input()

    for i, row in enumerate(grid):
        if "S" in row:
            start_position = (i, row.index("S"))
            break

    for pipe in "|-LJ7F":
        try:
            grid[start_position[0]][start_position[1]] = pipe
            return max(find_loop(grid, start_position).values()), pipe
        except ValueError:
            pass


def get_second_solution():
    grid = parse_input()

    for i, row in enumerate(grid):
        if "S" in row:
            start_position = (i, row.index("S"))
            break

    # Hard coded value of which pipe is under "S", printed from solving p1
    grid[start_position[0]][start_position[1]] = "7"

    loop_coords = find_loop(grid, start_position).keys()

    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if (y, x) not in loop_coords:
                grid[y][x] = " "

    inside_loop = set()
    # Any tile within the loop needs to cross the loop an odd number of times in
    # any direction before reaching the boundary of the grid
    for y, row in enumerate(grid):
        for x in range(len(row)):
            if grid[y][x] == " ":
                crossings = 0
                for c in accumulate(row[x:]):
                    # Only count a crossing if the loop does not double back on
                    # the same row
                    cc = c.replace("-", "")
                    if cc.endswith("|") or cc.endswith("FJ") or cc.endswith("L7"):
                        crossings += 1
                if crossings % 2 == 1:
                    inside_loop.add((y, x))

    return len(inside_loop)


print(get_first_solution())
print(get_second_solution())
