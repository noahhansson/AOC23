from utils import read_input
from itertools import cycle
from typing import Iterable
from math import lcm


def parse_input() -> tuple[Iterable[str], dict[str, tuple[str, ...]]]:
    inpt = read_input("8")

    instructions = list(inpt[0])

    maps = {}

    for row in inpt[2:]:
        key = row.split("=")[0].strip()
        rooms = tuple([room.strip(" ()") for room in row.split("=")[1].split(",")])

        maps[key] = rooms

    return cycle(instructions), maps


def get_first_solution():
    instructions, maps = parse_input()

    current_room = "AAA"
    steps = 0
    while current_room != "ZZZ":
        instruction = next(instructions)
        if instruction == "L":
            current_room = maps[current_room][0]
        elif instruction == "R":
            current_room = maps[current_room][1]
        steps += 1

    return steps


def get_second_solution():
    instructions, maps = parse_input()

    start_rooms = [room for room in maps.keys() if room.endswith("A")]
    steps = [0] * len(start_rooms)

    for i, start_room in enumerate(start_rooms):
        current_room = start_room
        while not current_room.endswith("Z"):
            instruction = next(instructions)
            if instruction == "L":
                current_room = maps[current_room][0]
            elif instruction == "R":
                current_room = maps[current_room][1]
            steps[i] += 1

    return lcm(*steps)


print(get_first_solution())
print(get_second_solution())
