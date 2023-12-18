from utils import read_input


def parse_input() -> list[tuple[str, int, str]]:
    inpt = read_input("18")

    instructions = []
    for row in inpt:
        instructions.append(
            (row.split(" ")[0], int(row.split(" ")[1]), row.split(" ")[2].strip("()"))
        )

    return instructions


def solve(instructions: list[tuple[str, int, str]]) -> int:
    # Shoelace formula
    n_exterior: int = 0
    area: float = 0
    (x, y) = (0, 0)
    for instruction in instructions:
        (dx, dy) = (0, 0)
        match instruction:
            case "U", steps, _:
                dy = -steps
            case "D", steps, _:
                dy = steps
            case "L", steps, _:
                dx = -steps
            case "R", steps, _:
                dx = steps
        area += 1 / 2 * (y + (y + dy)) * (x - (x + dx))
        n_exterior += steps
        (x, y) = (x + dx, y + dy)

    # Pick's theorem
    n_interior = area - n_exterior / 2 + 1

    return int(n_interior + n_exterior)


def get_first_solution() -> int:
    instructions = parse_input()
    return solve(instructions)


def get_second_solution() -> int:
    instructions = parse_input()
    directions = "RDLU"
    instructions_p2 = []
    for instruction in instructions:
        direction = directions[int(instruction[2][-1])]
        steps = int(instruction[2][1:-1], 16)
        instructions_p2.append((direction, steps, ""))

    return solve(instructions_p2)


print(get_first_solution())
print(get_second_solution())
