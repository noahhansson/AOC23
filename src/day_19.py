from utils import read_input
from typing import TypeAlias
from collections import deque

HypercubeType: TypeAlias = tuple[
    tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]
]


def parse_input() -> tuple[dict[str, list[str]], list[tuple[int, ...]]]:
    inpt = read_input("19")

    workflows: dict[str, list[str]] = {}

    for row in inpt[: inpt.index("")]:
        name = row.split("{")[0]
        workflows[name] = row.split("{")[1].strip("}").split(",")

    parts = []
    for row in inpt[inpt.index("") + 1 :]:
        parts.append(tuple(int(val.strip("xmas= {}")) for val in row.split(",")))

    return workflows, parts


def eval_instruction(inpt: tuple[int, int, int, int], instruction: str) -> str | None:
    if ">" not in instruction and "<" not in instruction:
        return instruction

    var = instruction[0]
    var_idx = "xmax".find(var)
    operator = instruction[1]
    threshold = int(instruction.split(":")[0][2:])
    ret = instruction.split(":")[1]

    if operator == ">":
        return ret if (inpt[var_idx] > threshold) else None

    if operator == "<":
        return ret if (inpt[var_idx] < threshold) else None

    return None


def eval_instruction_p2(
    inpt: HypercubeType, instruction: str
) -> tuple[tuple[HypercubeType, str | None], ...]:
    if ">" not in instruction and "<" not in instruction:
        return ((inpt, instruction),)

    var = instruction[0]
    var_idx = "xmas".find(var)
    operator = instruction[1]
    threshold = int(instruction.split(":")[0][2:])
    ret = instruction.split(":")[1]

    split_range = inpt[var_idx]

    if operator == ">":
        # range that passes
        r1 = (max(split_range[0], threshold + 1), split_range[1])
        # range that does not pass
        r2 = (split_range[0], min(split_range[1], threshold))

    if operator == "<":
        # range that passes
        r1 = (split_range[0], min(split_range[1], threshold - 1))
        # range that does not pass
        r2 = (max(split_range[0], threshold), split_range[1])

    # Cube that passes:
    c1 = tuple(inpt[i] if i != var_idx else r1 for i in range(4))
    c2 = tuple(inpt[i] if i != var_idx else r2 for i in range(4))

    return (c1, ret), (c2, None)


def get_first_solution() -> int:
    workflows, parts = parse_input()

    accepted = []

    for part in parts:
        location = "in"
        while location not in ("A", "R"):
            workflow = workflows[location]
            for instruction in workflow:
                if nxt := eval_instruction(part, instruction):
                    location = nxt
                    break
        if location == "A":
            accepted.append(part)

    return sum([sum([x for x in part]) for part in accepted])


def get_second_solution() -> int:
    workflows, _ = parse_input()
    items = ((1, 4000), (1, 4000), (1, 4000), (1, 4000))

    queue: deque[tuple[HypercubeType, str | None]] = deque()

    queue.append((items, "in"))

    accepted = []

    while queue:
        cube, workflow_name = queue.popleft()
        if workflow_name == "A":
            accepted.append(cube)
        elif workflow_name == "R":
            continue
        else:
            for instruction in workflows[workflow_name]:
                for x in eval_instruction_p2(cube, instruction):
                    if x[1]:
                        queue.append(x)
                    else:
                        cube = x[0]

    s = 0
    for cube in accepted:
        c = 1
        for rnge in cube:
            c *= rnge[1] - rnge[0] + 1
        s += c

    return s


print(get_first_solution())
print(get_second_solution())
