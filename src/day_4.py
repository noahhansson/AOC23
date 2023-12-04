from utils import read_input


def parse_inpt() -> list[list[set[int]]]:
    inpt = read_input("4")
    inpt_cleaned = [row.split(":")[1].split("|") for row in inpt]
    inpt_cleaned_2 = [
        [set([int(v) for v in vs.strip(" ").split(" ") if v != ""]) for vs in row]
        for row in inpt_cleaned
    ]

    return inpt_cleaned_2


def get_wins(game: list[set[int]]) -> int:
    numbers = game[0]
    winners = game[1]

    n_wins = len(numbers.intersection(winners))

    return n_wins


def get_first_solution():
    games = parse_inpt()
    total_score = 0

    for game in games:
        n_wins = get_wins(game)

        if n_wins > 0:
            total_score += 2 ** (n_wins - 1)

    return total_score


def get_second_solution():
    games = parse_inpt()

    total_cards = [1] * len(games)

    for i, n in enumerate(total_cards):
        wins = get_wins(games[i])
        for j in range(wins):
            total_cards[i + j + 1] += n
    return sum(total_cards)


print(get_first_solution())
print(get_second_solution())
