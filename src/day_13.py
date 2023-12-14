from utils import read_input

def parse_input() -> list[set[tuple[int, int]]]:
    inpt = read_input("13")

    patterns: list[set[tuple[int, int]]] = list()
    buffer: set[tuple[int, int]] = set()

    y = 0
    for row in inpt:
        if row == "":
            patterns.append(buffer)
            buffer = set()
            y = 0
        else:
            for x, c in enumerate(row):
                if c == "#":
                    buffer.add((x, y))
            y += 1
    else:
        patterns.append(buffer)

    return patterns

def transpose_pattern(pattern: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return {(y, x) for x, y in pattern}

def find_reflection(pattern: set[tuple[int, int]], p2: bool = False) -> int:
    return reflect(pattern, p2) + 100 * reflect(transpose_pattern(pattern), p2)

def reflect(pattern: set[tuple[int, int]], p2: bool = False) -> int:
    xmin = min([x for x, _ in pattern])
    xmax = max([x for x, _ in pattern])

    for xr in range(xmin, xmax):
        left_half = {coord for coord in pattern if coord[0] <= xr}
        right_half = {
            (2 * xr + 1 - coord[0], coord[1]) for coord in pattern if coord[0] > xr
        }

        x_intersect = {coord[0] for coord in right_half}.intersection(
            coord[0] for coord in left_half
        )
        left_half_overlap = {coord for coord in left_half if coord[0] in x_intersect}
        right_half_overlap = {coord for coord in right_half if coord[0] in x_intersect}

        if not p2:
            if x_intersect and (left_half_overlap == right_half_overlap):
                return xr + 1
        else:
            if x_intersect and (
                (
                    len(left_half_overlap - right_half_overlap) == 1
                    and (len(right_half_overlap - left_half_overlap) == 0)
                )
                or (
                    len(right_half_overlap - left_half_overlap) == 1
                    and (len(left_half_overlap - right_half_overlap) == 0)
                )
            ):
                return xr + 1

    return 0

print(sum([find_reflection(pattern) for pattern in parse_input()]))
print(sum([find_reflection(pattern, p2=True) for pattern in parse_input()]))
