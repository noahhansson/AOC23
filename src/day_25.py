from utils import read_input
from collections import defaultdict, deque, Counter
from itertools import combinations, cycle
from random import random


def parse_input() -> dict[str, set[str]]:
    inpt = read_input("25")
    connections: dict[str, set[str]] = defaultdict(set[str])

    for row in inpt:
        left = row.split(":")[0]
        right = set([s for s in row.split(":")[1].strip(" ").split(" ")])

        for r in right:
            connections[left].add(r)
            connections[r].add(left)

    return connections


def calculate_edges(start: str, connections: dict[str, set[str]]) -> int:
    visited: set[str] = set()
    queue: list[str] = []

    queue.append(start)

    while queue:
        edge = queue.pop()
        visited.add(edge)

        for connected_edge in connections[edge]:
            if connected_edge not in visited:
                queue.append(connected_edge)

    return len(visited)


def find_path(
    start: str, stop: str, connections: dict[str, set[str]]
) -> list[str] | None:
    #BFS search
    queue: deque[list[str]] = deque()
    queue.append([start])

    while queue:
        path = queue.popleft()
        position = path[-1]

        if position == stop:
            return path

        connected = connections[position]
        for edge in connected:
            if edge not in path:
                queue.append(path + [edge])

    return None


def get_first_solution():
    connections = parse_input()
    total_edges = calculate_edges(list(connections.keys())[0], connections)
    vertice_count = []

    cuts = []

    all_edges = list(connections.keys())
    combs = sorted(list(combinations(all_edges, 2)), key=lambda x: random())

    for i, (start, stop) in enumerate(cycle(combs)):
        path = find_path(start, stop, connections)
        vertice_count += [tuple(sorted([e1, e2])) for e1, e2 in zip(path, path[1:])]

        # Number of iterations before cutting. Might need tweaking
        if i % 15 == 0 and i > 0:
            cut = Counter(vertice_count).most_common(1)[0][0]

            print(f"cutting {cut}")

            connections[cut[0]] = connections[cut[0]] - {cut[1]}
            connections[cut[1]] = connections[cut[1]] - {cut[0]}

            vertice_count = []
            cuts.append(cut)

            if len(cuts) == 3:
                break

    e1 = calculate_edges(cuts[0][1], connections)
    e2 = calculate_edges(cuts[0][0], connections)

    if e1 + e2 == total_edges:
        return e1 * e2
    else:
        raise RuntimeError("Solution did not work, try upping iteration count")


print(get_first_solution())
