from utils import read_input

inpt = read_input("1")

def get_first_solution():
    s = 0
    for line in inpt:
        numbers = "".join([x for x in line if x.isnumeric()])
        s += int(numbers[0] + numbers[-1])

    return s

def get_second_solution():
    s = 0

    int_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    for line in inpt:
        line_fixed = ""
        for c in line:
            line_fixed += c
            for key, value in int_map.items():
                if line_fixed.endswith(key):
                    line_fixed = line_fixed.replace(key, f"{key}{value}{key}")

        numbers = "".join([x for x in line_fixed if x.isnumeric()])
        s += int(numbers[0] + numbers[-1])

    return s


print(get_first_solution())
print(get_second_solution())
