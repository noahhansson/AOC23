from __future__ import annotations
from utils import read_input
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Brick:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    def fall(self, other_bricks: list[Brick]) -> bool:
        bricks_below: list[Brick] = []

        for brick in other_bricks:
            z_below = min(self.z) > max(brick.z)
            x_overlap = (min(self.x) <= max(brick.x)) and (max(self.x) >= min(brick.x))
            y_overlap = (min(self.y) <= max(brick.y)) and (max(self.y) >= min(brick.y))

            if z_below and x_overlap and y_overlap:
                bricks_below.append(brick)

        if bricks_below:
            z_dist = min([min(self.z) - max(brick.z) for brick in bricks_below]) - 1
        else:
            z_dist = min(self.z) - 1

        if z_dist > 0:
            self.z = (self.z[0] - z_dist, self.z[1] - z_dist)
            return True

        return False

    def supports(self, other_bricks: Iterable[Brick]) -> set[Brick]:
        bricks_above: set[Brick] = set()

        for brick in other_bricks:
            z_above = max(self.z) == (min(brick.z) - 1)
            x_overlap = (min(self.x) <= max(brick.x)) and (max(self.x) >= min(brick.x))
            y_overlap = (min(self.y) <= max(brick.y)) and (max(self.y) >= min(brick.y))

            if z_above and x_overlap and y_overlap:
                bricks_above.add(brick)

        return bricks_above

    def supported_by(self, other_bricks: Iterable[Brick]) -> set[Brick]:
        bricks_above: set[Brick] = set()

        for brick in other_bricks:
            z_below = min(self.z) == (max(brick.z) + 1)
            x_overlap = (min(self.x) <= max(brick.x)) and (max(self.x) >= min(brick.x))
            y_overlap = (min(self.y) <= max(brick.y)) and (max(self.y) >= min(brick.y))

            if z_below and x_overlap and y_overlap:
                bricks_above.add(brick)

        return bricks_above

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.z)


def parse_input() -> list[Brick]:
    inpt = read_input("22")
    bricks: list[Brick] = []

    for row in inpt:
        x0, y0, z0 = row.split("~")[0].split(",")
        x1, y1, z1 = row.split("~")[1].split(",")
        bricks.append(Brick((int(x0), int(x1)), (int(y0), int(y1)), (int(z0), int(z1))))

    return sorted(bricks, key=lambda x: min(x.z))


def get_first_solution():
    bricks = parse_input()

    for brick in bricks:
        brick.fall(bricks)

    n_safe = 0
    for brick in bricks:
        supported_bricks = brick.supports(bricks)
        if all(
            [
                len(supported_brick.supported_by(bricks)) > 1
                for supported_brick in supported_bricks
            ]
        ):
            n_safe += 1

    return n_safe


def get_falling(bricks: list[Brick], disintegraded: Brick) -> set[Brick]:
    falling = set()
    not_falling = set(bricks) - {disintegraded}

    queue: list[Brick] = []

    for supported_brick in disintegraded.supports(not_falling):
        if not supported_brick.supported_by(not_falling):
            falling.add(supported_brick)
            if supported_brick not in queue:
                queue.append(supported_brick)
            not_falling.remove(supported_brick)

    while queue:
        falling_brick = queue.pop()
        for supported_brick in falling_brick.supports(not_falling):
            if not supported_brick.supported_by(not_falling):
                falling.add(supported_brick)
                if supported_brick not in queue:
                    queue.append(supported_brick)
                not_falling.remove(supported_brick)

    return falling


def get_second_solution():
    bricks = parse_input()

    for brick in bricks:
        brick.fall(bricks)

    ans = 0

    for brick in bricks:
        ans += len(get_falling(bricks, brick))

    return ans


print(get_first_solution())
print(get_second_solution())
