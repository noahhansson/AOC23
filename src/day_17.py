from utils import read_input
import heapq


def parse_input() -> dict[tuple[int, int], int]:
    inpt = read_input("17")

    costs = {}
    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            costs[(x, y)] = int(c)

    return costs


def get_neighbours(
    pos: tuple[int, int],
    costs: dict[tuple[int, int], int],
    path: list[str],
    p2: bool = False,
) -> list[tuple[tuple[int, int], str]]:
    neighbours = []

    lookback = 3 if not p2 else 10
    prev_steps = set(path[-lookback:])
    straight_line = len(prev_steps) == 1
    uncomplete_line = len(set(path[-4:])) > 1

    opposites = {
        "left": "right",
        "right": "left",
        "up": "down",
        "down": "up",
    }

    for dx, dy, direction in (
        (-1, 0, "left"),
        (1, 0, "right"),
        (0, -1, "up"),
        (0, 1, "down"),
    ):
        if (pos[0] + dx, pos[1] + dy) in costs.keys():
            if (
                not (straight_line and direction in prev_steps)
                and opposites.get(path[-1]) != direction
                and not (p2 and uncomplete_line and direction != path[-1])
            ):
                neighbours.append(((pos[0] + dx, pos[1] + dy), direction))

    return neighbours


def dijkstra(
    start_pos: tuple[int, int],
    target_pos: tuple[int, int],
    costs: dict[tuple[int, int], int],
    p2: bool = False,
) -> int:
    lookback = 3 if not p2 else 10

    seen: set[tuple[tuple[int, int], tuple[str, ...]]] = set()
    queue: list[tuple[int, tuple[int, int], list[str]]] = []
    heapq.heapify(queue)

    path: list[str] = [""] * lookback
    heapq.heappush(queue, (0, start_pos, path))

    seen.add((start_pos, tuple(path[-lookback:])))

    while queue:
        cost, position, path = heapq.heappop(queue)

        if position == target_pos:
            if len(set(path[-4:])) > 1:
                continue
            return cost

        neighbours = get_neighbours(position, costs, path, p2)

        for neighbour, direction in neighbours:
            n_cost = cost + costs[neighbour]

            key = (neighbour, tuple(path[-(lookback - 1) :] + [direction]))
            if key not in seen:
                seen.add(key)
                heapq.heappush(queue, (n_cost, neighbour, path + [direction]))

    return -1


def get_first_solution() -> int:
    costs = parse_input()

    start_pos = (0, 0)
    yy = max([y for x, y in costs.keys()])
    xx = max([x for x, y in costs.keys()])
    target_pos = (xx, yy)

    return dijkstra(start_pos, target_pos, costs)


def get_second_solution() -> int:
    costs = parse_input()

    start_pos = (0, 0)
    yy = max([y for x, y in costs.keys()])
    xx = max([x for x, y in costs.keys()])
    target_pos = (xx, yy)

    return dijkstra(start_pos, target_pos, costs, p2=True)


print(get_first_solution())
print(get_second_solution())
