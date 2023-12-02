from utils import read_input


DrawType = tuple[int, int, int]

def get_cleaned_input() -> list[list[DrawType]]:
    inpt = read_input("2.txt")

    #Drop "Game x:"
    inpt_cleaned = [
        row.split(":")[1].strip(" ") for row in inpt
    ]

    #Split each reveal
    inpt_cleaned_2 = [
        row.split(";") for row in inpt_cleaned
    ]

    #Convert each reveal to a tuple
    inpt_cleaned_3 = [
        [
            str_to_tuple(draw)
            for draw in game
        ]
        for game in inpt_cleaned_2
    ]
    return inpt_cleaned_3


def str_to_tuple(inpt_str: str) -> DrawType:
    red = 0
    green = 0
    blue = 0

    inpt_list = inpt_str.split(",")

    for val in inpt_list:
        match val.strip(" ").split(" "):
            case [x, "red"]:
                red += int(x)
            case [x, "green"]:
                green += int(x)
            case [x, "blue"]:
                blue += int(x)


    return (red, green, blue)


def get_first_solution():
    inpt_cleaned = get_cleaned_input()
    limits = (12, 13, 14)

    score = 0
    for i, game in enumerate(inpt_cleaned):
        possible = True

        for draw in game:
            if any(d > m for d, m in zip(draw, limits)):
                possible = False

        if possible:
            score += (i+1)
    
    return score


def get_second_solution():
    inpt_cleaned = get_cleaned_input()

    sum_power = 0

    for game in inpt_cleaned:
        max_cubes = [0, 0, 0]

        power = 1

        for draw in game:
            for i in range(3):
                if draw[i] > max_cubes[i]:
                    max_cubes[i] = draw[i]

        for i in range(3):
            power *= max_cubes[i]

        sum_power += power

    return sum_power


print(get_first_solution())
print(get_second_solution())
