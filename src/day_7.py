from utils import read_input
from functools import cmp_to_key
from collections import defaultdict


def parse_input() -> list[tuple[str, int]]:
    inpt = read_input("7")

    inpt_parsed = [row.split(" ") for row in inpt]
    inpt_parsed_2 = [(row[0], int(row[1])) for row in inpt_parsed]

    return inpt_parsed_2


def get_type(hand: str, joker_rule: bool = False) -> int:
    counter: dict[str, int] = defaultdict(int)

    for card in hand:
        counter[card] += 1

    if not joker_rule:
        values = list(counter.values())
    else:
        jokers = counter["J"]
        counter = {key: value for key, value in counter.items() if not key == "J"}
        try:
            values = list(counter.values())
            max_value_idx = values.index(max(values))
            values[max_value_idx] += jokers
        except ValueError:
            "JJJJJ"
            values = [5]

    if 5 in values:
        return 6
    elif 4 in values:
        return 5
    elif (3 in values) and (2 in values):
        return 4
    elif 3 in values:
        return 3
    elif values.count(2) == 2:
        return 2
    elif 2 in values:
        return 1

    return 0


def compare_values(hand_1: str, hand_2: str, joker_rule: bool = False) -> int:
    def _value_to_int(card: str):
        if card == "A":
            return 14
        elif card == "K":
            return 13
        elif card == "Q":
            return 12
        elif card == "J":
            if joker_rule:
                return 0
            else:
                return 11
        elif card == "T":
            return 10
        else:
            return int(card)

    for c1, c2 in zip(hand_1, hand_2):
        v1 = _value_to_int(c1)
        v2 = _value_to_int(c2)

        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    return 0


def compare_hands(hand_1: str, hand_2: str) -> int:
    type_1 = get_type(hand_1)
    type_2 = get_type(hand_2)

    if type_1 > type_2:
        return 1
    elif type_1 < type_2:
        return -1
    else:
        return compare_values(hand_1, hand_2)


def compare_hands_2(hand_1: str, hand_2: str) -> int:
    type_1 = get_type(hand_1, joker_rule=True)
    type_2 = get_type(hand_2, joker_rule=True)

    if type_1 > type_2:
        return 1
    elif type_1 < type_2:
        return -1

    return compare_values(hand_1, hand_2, joker_rule=True)


def get_first_solution():
    hands = parse_input()
    hands_sorted = sorted(hands, key=cmp_to_key(lambda x, y: compare_hands(x[0], y[0])))

    scores = 0
    for i, hand in enumerate(hands_sorted):
        scores += (i + 1) * hand[1]

    return scores


def get_second_solution():
    hands = parse_input()
    hands_sorted = sorted(
        hands, key=cmp_to_key(lambda x, y: compare_hands_2(x[0], y[0]))
    )

    scores = 0
    for i, hand in enumerate(hands_sorted):
        scores += (i + 1) * hand[1]

    return scores


print(get_first_solution())
print(get_second_solution())
