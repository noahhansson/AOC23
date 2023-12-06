from utils import read_input


def parse_input() -> tuple[list[int], list[int]]:
    inpt = read_input("6")
    times = [int(x) for x in inpt[0].split()[1:]]
    distances = [int(x) for x in inpt[1].split()[1:]]
    return times, distances


def parse_input_2() -> tuple[int, int]:
    inpt = read_input("6")
    time = int("".join(inpt[0].split()[1:]))
    distance = int("".join(inpt[1].split()[1:]))
    return time, distance


def get_first_solution() -> int:
    total_wins = []
    for time, min_distance in zip(*parse_input()):
        n_wins = 0
        for h in range(1, time):
            d = h * max(time - h, 0)
            if d > min_distance:
                n_wins += 1
        total_wins.append(n_wins)

    p = 1
    for d in total_wins:
        p *= d

    return p


def get_second_solution() -> int:
    time, min_distance = parse_input_2()
    n_wins = 0
    for h in range(1, time):
        d = h * max(time - h, 0)
        if d > min_distance:
            n_wins += 1
    return n_wins


print(get_first_solution())
print(get_second_solution())
