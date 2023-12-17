from utils import read_input
import heapq


def parse_input() -> tuple[dict[tuple[int, int], int], tuple[int, int]]:
    inpt = read_input("17")

    costs = {}
    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            costs[(x, y)] = int(c)

    return costs, (x,y)


def get_neighbours(
    pos: tuple[int, int],
    costs: dict[tuple[int, int], int],
    prev_direction: str,
    p2: bool = False,
) -> list[tuple[tuple[int, int], int, list[str]]]:
    neighbours = []

    max_dist = 10 if p2 else 3
    min_dist = 4 if p2 else 1

    for dx, dy, direction, opposite in (
        (-1, 0, "left", "right"),
        (1, 0, "right", "left"),
        (0, -1, "up", "down"),
        (0, 1, "down", "up"),
    ):
        cost = 0
        if prev_direction not in (direction, opposite):
            for steps in range(1, max_dist + 1):
                next_pos = (pos[0] + dx * steps, pos[1] + dy * steps)
                if next_pos in costs.keys():
                    cost += costs[next_pos]
                    if steps >= min_dist:
                        neighbours.append((next_pos, cost, [direction] * steps))

    return neighbours


def dijkstra(
    start_pos: tuple[int, int],
    target_pos: tuple[int, int],
    costs: dict[tuple[int, int], int],
    p2: bool = False,
) -> int:
    
    # {((x, y), prev_direction): cost}
    seen: dict[tuple[tuple[int, int], str], int] = {}
    path: list[str] = [""]

    queue: list[tuple[int, tuple[int, int], list[str]]] = []
    heapq.heapify(queue)
    heapq.heappush(queue, (0, start_pos, path))

    seen[(start_pos, path[-1])] = 0

    while queue:
        cost, position, path = heapq.heappop(queue)

        if position == target_pos:
            return cost

        neighbours = get_neighbours(position, costs, path[-1], p2)

        for neighbour, n_cost, directions in neighbours:
            key = (neighbour, directions[-1])
            if key not in seen.keys() or seen[key] > cost + n_cost:
                seen[key] = cost + n_cost
                heapq.heappush(queue, (cost + n_cost, neighbour, path + directions))

    return -1


def get_first_solution() -> int:
    costs, target = parse_input()

    return dijkstra((0, 0), target, costs)


def get_second_solution() -> int:
    costs, target = parse_input()

    return dijkstra((0, 0), target, costs, p2=True)


print(get_first_solution())
print(get_second_solution())
