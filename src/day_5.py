from utils import read_input

MapType = list[list[int]]

def parse_input() -> tuple[list[int], list[MapType]]:
    inpt = read_input("5")

    seeds  = [int(x) for x in inpt[0].split(" ")[1:]]

    maps = []
    buffer = []
    map_name = ""

    for row in inpt[2:]:
        if "map" in row:
            continue
        elif row != "":
            buffer.append([int(x) for x in row.split(" ")])
        elif row == "":
            maps.append(buffer)
            buffer = []
    else:
        maps.append(buffer)
        buffer = []

    return seeds, maps

def solve_seed(seed: int, maps: list[MapType]) -> int:
    position = seed

    for mp in maps:
        for row in mp:
            map_destination = row[0]
            map_source = row[1]
            map_range = row[2]

            if (position >= map_source) and (position < map_source + map_range):
                destination = (position - map_source) + map_destination
                position = destination
                break

    return position

def solve_seed_ranges(seed_ranges: list[tuple[int, int]], maps: list[MapType]) -> list[tuple[int, int]]:
    
    next_iter_ranges = seed_ranges.copy()

    for mp in maps:
        current_ranges = next_iter_ranges.copy()
        next_iter_ranges = []
        while current_ranges:

            seed_range = current_ranges.pop()

            for row in mp:
                map_destination = row[0]
                map_source = row[1]
                map_range = row[2]
                map_source_max = map_source + map_range - 1

                if (seed_range[0] >= map_source) and (seed_range[1] < map_source + map_range):
                    #Overlap while range
                    next_iter_ranges.append((
                        seed_range[0] - map_source + map_destination,
                        seed_range[1] - map_source + map_destination
                    ))

                    break

                elif (map_source <= seed_range[1]) and (seed_range[1] <= map_source_max):
                    #Seed range right edge overlaps with map

                    overlap_range = (map_source, seed_range[1])
                    no_overlap_range = (seed_range[0], map_source - 1)

                    next_iter_ranges.append((
                        overlap_range[0] - map_source + map_destination,
                        overlap_range[1] - map_source + map_destination
                    ))

                    current_ranges.append(no_overlap_range)

                    break

                elif (seed_range[0] < map_source_max) and not (seed_range[0] < map_source):
                    #Seed range left edge overlaps with map

                    overlap_range = (seed_range[0], map_source_max)
                    no_overlap_range = (map_source_max + 1, seed_range[1])

                    next_iter_ranges.append((
                        overlap_range[0] - map_source + map_destination,
                        overlap_range[1] - map_source + map_destination
                    ))

                    current_ranges.append(no_overlap_range)

                    break

            else:
                next_iter_ranges.append(seed_range)

    return next_iter_ranges

def get_first_solution():
    seeds, maps = parse_input()

    final_positions = [-1] * len(seeds)

    for i, seed in enumerate(seeds):

        final_positions[i] = solve_seed(seed, maps)

    return min(final_positions)


def get_second_solution():
    seeds, maps = parse_input()

    seed_starts = seeds[::2]
    range_lengths = seeds[1::2]

    seed_ranges = [
        (start, start + length - 1) for start, length in zip(seed_starts, range_lengths)
    ]

    res = solve_seed_ranges(seed_ranges, maps)

    return min([r[0] for r in res])

print(get_first_solution())
print(get_second_solution())
