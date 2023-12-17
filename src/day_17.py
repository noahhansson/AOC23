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
    pos: tuple[int, int], costs: dict[tuple[int, int], int], path: list[str]
) -> list[tuple[tuple[int, int], str]]:
    neighbours = []

    if len(path) >= 3:
        prev_steps = set(path[-3:])
        straight_line = len(prev_steps) == 1
    else:
        straight_line = False

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
                not (straight_line 
                and direction in prev_steps)
                and opposites.get(path[-1]) != direction 
            ):
                neighbours.append(((pos[0] + dx, pos[1] + dy), direction))

    return neighbours

def taxicab(pos: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

def dijkstra(
    start_pos: tuple[int, int],
    target_pos: tuple[int, int],
    costs: dict[tuple[int, int], int],
) -> int:
    
    seen: set[tuple[tuple[int, int], tuple[str, ...]]] = set()
    queue: list[tuple[int, tuple[int, int], list[str]]] = []
    heapq.heapify(queue)

    path: list[str] = ["", "", ""]
    heapq.heappush(queue, (0, start_pos, path))

    seen.add((start_pos, tuple(path[-3:])))

    while queue:
        cost, position, path = heapq.heappop(queue)

        print(cost, position)
        if position == target_pos:
            return cost

        neighbours = get_neighbours(position, costs, path)

        for neighbour, direction in neighbours:
            n_cost = cost + costs[neighbour]

            if ((neighbour, tuple(path[-2:] + [direction])) not in seen):
                seen.add((neighbour, tuple(path[-2:] + [direction])))
                heapq.heappush(queue, (n_cost, neighbour, path + [direction]))

    return -1


def get_first_solution():
    costs = parse_input()

    start_pos = (0, 0)
    yy = max([y for x, y in costs.keys()])
    xx = max([x for x, y in costs.keys()])
    target_pos = (xx, yy)

    return dijkstra(start_pos, target_pos, costs)


def get_second_solution():
    pass


print(get_first_solution())
print(get_second_solution())
