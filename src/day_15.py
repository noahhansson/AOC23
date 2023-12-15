from utils import read_input


def parse_input() -> list[str]:
    inpt = read_input("15")
    return inpt[0].split(",")


def encode(s: str) -> int:
    n = 0
    for c in s:
        n += ord(c)
        n *= 17
        n = n % 256

    return n


def get_label(s: str) -> str:
    if "=" in s:
        return s.split("=")[0]
    elif "-" in s:
        return s.split("-")[0]
    raise ValueError


def calc_focusing_power(boxes: list[list[tuple[str, int]]]) -> int:
    score = 0
    for i, lenses in enumerate(boxes):
        for j, lens in enumerate(lenses):
            score += (i + 1) * (j + 1) * lens[1]

    return score


def get_first_solution() -> int:
    return sum([encode(s) for s in parse_input()])


def get_second_solution() -> int:
    steps = parse_input()

    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for step in steps:
        box_idx = encode(get_label(step))
        contents = boxes[box_idx]
        if "=" in step:
            label, focal_length = step.split("=")

            if any([label == lens[0] for lens in contents]):
                new_contents = [
                    lens if (label != lens[0]) else (label, int(focal_length))
                    for lens in contents
                ]
                boxes[box_idx] = new_contents

            else:
                contents.append((label, int(focal_length)))

        elif "-" in step:
            label = step.split("-")[0]

            if any([label == lens[0] for lens in contents]):
                new_contents = [lens for lens in contents if (label != lens[0])]
                boxes[box_idx] = new_contents

    return calc_focusing_power(boxes)


print(get_first_solution())
print(get_second_solution())
