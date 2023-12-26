from __future__ import annotations
from utils import read_input
from typing import TypeAlias

NodeType: TypeAlias = tuple[int, int]


class Graph:
    connections: dict[NodeType, dict[NodeType, int]]

    def __init__(self) -> None:
        self.connections = {}

    def connect(self, n1: NodeType, n2: NodeType, cost: int):
        if n1 not in self.connections:
            self.connections[n1] = {}
        self.connections[n1][n2] = cost

    def get_neighbours(self, node: NodeType) -> dict[NodeType, int]:
        return self.connections[node]

    def __repr__(self):
        return f"{type(self).__name__}({self.connections})"


def parse_input(p2: bool = False) -> tuple[Graph, NodeType, NodeType]:
    inpt = read_input("23")

    paths = set()
    slopes = dict()
    visited = set()

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == ".":
                paths.add((x, y))
            if c in ("<>v^"):
                slopes[(x, y)] = c

    start = [(x, y) for x, y in paths if y == 0][0]
    end = (x - 1, y)
    nodes = [start]

    graph = Graph()

    while nodes:
        node = nodes.pop()
        visited.add(node)
        neighbours = get_neighbours(node, paths, slopes, set(), p2)
        for neighbour in neighbours:
            adj_node, cost = find_connection(
                neighbour, paths, slopes, seen={node}, p2=p2
            )

            graph.connect(node, adj_node, cost)

            if adj_node not in visited:
                nodes.append(adj_node)

    return graph, start, end


def find_connection(
    start: NodeType,
    paths: set[NodeType],
    slopes: dict[NodeType, str],
    seen: set[NodeType],
    p2: bool = False,
) -> tuple[NodeType, int]:
    path_length = 1
    pos = start

    while len(neighbours := get_neighbours(pos, paths, slopes, seen, p2)) == 1:
        if not p2 and pos in slopes:
            return (pos, path_length)

        seen.add(pos)
        path_length += 1
        pos = next(iter(neighbours))

    if len(neighbours) == 0:
        return (pos, path_length)

    if len(neighbours) > 1:
        return (pos, path_length)

    raise RuntimeError


def get_neighbours(
    pos: tuple[int, int],
    paths: set[tuple[int, int]],
    slopes: dict[tuple[int, int], str],
    seen: set[tuple[int, int]] = set(),
    p2: bool = False,
) -> set[tuple[int, int]]:
    neighbours: set[tuple[int, int]] = set()
    directions: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
    if (not p2) and (pos in slopes):
        if slopes[pos] == "<":
            directions = ((-1, 0),)
        elif slopes[pos] == ">":
            directions = ((1, 0),)
        elif slopes[pos] == "v":
            directions = ((0, 1),)
        elif slopes[pos] == "^":
            directions = ((0, -1),)

    for dx, dy in directions:
        next_pos = (pos[0] + dx, pos[1] + dy)
        if (next_pos in paths or next_pos in slopes) and next_pos not in seen:
            neighbours.add(next_pos)

    return neighbours


def longest_path(
    graph: Graph,
    start: NodeType,
    target: NodeType,
    visited: set[NodeType] = set(),
    length: int = 0,
):
    if start == target:
        return length

    paths = []
    for neighbour, cost in graph.get_neighbours(start).items():
        if neighbour not in visited:
            paths.append(
                longest_path(
                    graph, neighbour, target, visited | {start}, length=length + cost
                )
            )

    return max([-1, *paths])


def get_first_solution():
    graph, start, end = parse_input(p2=False)
    return longest_path(graph, start, target=end)


def get_second_solution():
    graph, start, end = parse_input(p2=True)
    return longest_path(graph, start, target=end)


print(get_first_solution())
print(get_second_solution())
