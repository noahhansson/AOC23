from utils import read_input
from functools import cache
from typing import TypeAlias

SpringType: TypeAlias = str
CriterionType: TypeAlias = tuple[int, ...]


def parse_input() -> tuple[list[SpringType], list[CriterionType]]:
    inpt = read_input("12")

    springs = [row.split(" ")[0] for row in inpt]
    criteria = [tuple([int(x) for x in row.split(" ")[1].split(",")]) for row in inpt]

    return springs, criteria

@cache
def find_solutions(spring: SpringType, criterion: CriterionType) -> int:
    if (not criterion) and ("#" not in spring):
        return 1
    elif not (spring.replace(".", "") or criterion):
        return 1
    elif not (spring.replace(".", "") and criterion):
        return 0

    # Trim empty spaces
    if spring[0] == ".":
        return find_solutions(spring[1:], criterion)

    # Evaluate number of solutions for each possible symbol
    elif spring[0] == "?":
        return find_solutions("#" + spring[1:], criterion) + find_solutions(
            "." + spring[1:], criterion
        )

    elif spring[0] == "#":
        c = criterion[0]

        if spring.replace("?", "#").startswith("#" * c):
            # End of spring, return solvable if no criteria remain
            if len(spring) == c:
                if len(criterion) == 1:
                    return 1
                else:
                    return 0

            elif spring[c] == ".":
                new_spring = spring[c:]
                new_criteria = tuple([x for x in criterion[1:]])
                return find_solutions(new_spring, new_criteria)

            # After matching the next unknown must be operational
            elif spring[c] == "?":
                new_spring = spring[(c + 1) :]
                new_criteron = tuple([x for x in criterion[1:]])
                return find_solutions(new_spring, new_criteron)

        else:
            return 0

    return 0


def get_first_solution():
    return sum(
        [
            find_solutions(spring, criterion)
            for spring, criterion in zip(*parse_input())
        ]
    )


def get_second_solution():
    springs, criteria = parse_input()

    springs = ["?".join([spring] * 5) for spring in springs]
    criteria = [criterion * 5 for criterion in criteria]

    return sum(
        [
            find_solutions(spring, criterion)
            for spring, criterion in zip(springs, criteria)
        ]
    )


print(get_first_solution())
print(get_second_solution())
