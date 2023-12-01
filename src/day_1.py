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
    for line in inpt:
        line_fixed = ""
        for c in line:
            line_fixed += c
            if line_fixed.endswith("one"):
                line_fixed = line_fixed.replace("one", "1")
            elif line_fixed.endswith("two"):
                line_fixed = line_fixed.replace("two", "2")
            elif line_fixed.endswith("three"):
                line_fixed = line_fixed.replace("three", "3")
            elif line_fixed.endswith("four"):
                line_fixed = line_fixed.replace("four", "4")
            elif line_fixed.endswith("five"):
                line_fixed = line_fixed.replace("five", "5")
            elif line_fixed.endswith("six"):
                line_fixed = line_fixed.replace("six", "6")
            elif line_fixed.endswith("seven"):
                line_fixed = line_fixed.replace("seven", "7")
            elif line_fixed.endswith("eight"):
                line_fixed = line_fixed.replace("eight", "8")
            elif line_fixed.endswith("nine"):
                line_fixed = line_fixed.replace("nine", "9")

        numbers = "".join([x for x in line_fixed if x.isnumeric()])
        s += int(numbers[0] + numbers[-1])

    return s


print(get_first_solution())
print(get_second_solution())
