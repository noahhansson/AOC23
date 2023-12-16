from utils import read_input
from typing import TypeAlias

LayoutType: TypeAlias = dict[tuple[int, int], str]


def parse_input() -> tuple[LayoutType, tuple[int, int]]:
    inpt = read_input("16")

    layout = {}
    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c in ("/\-|"):
                layout[(x, y)] = c

    return layout, (x, y)


def beam(
    position: tuple[int, int],
    direction: tuple[int, int],
    layout: LayoutType,
    grid_size: tuple[int, int],
) -> set[tuple[int, int]]:
    _called = set()

    def _beam(
        position: tuple[int, int],
        direction: tuple[int, int],
        layout: LayoutType,
        grid_size: tuple[int, int],
    ) -> set[tuple[int, int]]:
        if (position, direction) in _called:
            return set()
        else:
            _called.add((position, direction))

        seen = set()
        seen.add(position)

        while True:
            position = (position[0] + direction[0], position[1] + direction[1])

            if (
                position[0] > grid_size[0]
                or position[1] > grid_size[1]
                or position[0] < 0
                or position[1] < 0
            ):
                break
            else:
                seen.add(position)

            if position in layout.keys():
                if layout[position] == "\\":
                    new_direction = (direction[1], direction[0])
                    seen = seen | _beam(position, new_direction, layout, grid_size)
                    break

                if layout[position] == "/":
                    new_direction = (-direction[1], -direction[0])
                    seen = seen | _beam(position, new_direction, layout, grid_size)
                    break

                if layout[position] == "-":
                    if direction in ((0, 1), (0, -1)):
                        for new_direction in ((1, 0), (-1, 0)):
                            seen = seen | _beam(
                                position, new_direction, layout, grid_size
                            )
                        break

                if layout[position] == "|":
                    if direction in ((1, 0), (-1, 0)):
                        for new_direction in ((0, 1), (0, -1)):
                            seen = seen | _beam(
                                position, new_direction, layout, grid_size
                            )
                        break

        return seen

    return _beam(position, direction, layout, grid_size)


def get_first_solution():
    layout, grid_size = parse_input()

    start_pos = (-1, 0)
    direction = (1, 0)

    return len(beam(start_pos, direction, layout, grid_size)) - 1


def get_second_solution():
    layout, grid_size = parse_input()

    scores = []

    for y in range(0, grid_size[1] + 1):
        start_pos = (-1, y)
        direction = (1, 0)
        scores.append(len(beam(start_pos, direction, layout, grid_size)) - 1)

        start_pos = (grid_size[0] + 1, y)
        direction = (-1, 0)
        scores.append(len(beam(start_pos, direction, layout, grid_size)) - 1)

    for x in range(0, grid_size[0] + 1):
        start_pos = (x, -1)
        direction = (0, 1)
        scores.append(len(beam(start_pos, direction, layout, grid_size)) - 1)

        start_pos = (x, grid_size[1] + 1)
        direction = (0, -1)
        scores.append(len(beam(start_pos, direction, layout, grid_size)) - 1)

    return max(scores)


print(get_first_solution())
print(get_second_solution())
