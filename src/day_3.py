from utils import read_input
from dataclasses import dataclass
from itertools import product

Coordinate = tuple[int, int]

@dataclass(frozen=True)
class Symbol:
    position: Coordinate
    value: str

    def get_adjacent(self, numbers: set["Number"]) -> set["Number"]:
        return set([number for number in numbers if number.is_adjacent(self)])


@dataclass(frozen=True)
class Number:
    positions: tuple[Coordinate, ...]
    value: int

    def is_adjacent(self, symbol: "Symbol") -> bool:
        for dx, dy in product((-1, 0, 1), repeat=2):
            if (symbol.position[0] + dx, symbol.position[1] + dy) in set(self.positions):
                return True
            
        return False

def parse_inpt() -> tuple[set[Symbol], set[Number]]:
    inpt = read_input("3")

    symbols = set()
    for i, row in enumerate(inpt):
        for j, c in enumerate(row):
            if (not c.isnumeric()) and (c != "."):
                symbols.add(Symbol(position=(i, j), value=c))

    numbers = set()

    for i, row in enumerate(inpt):
        current_number: list[str] = []
        current_positions: list[Coordinate] = []
        for j, c in enumerate(row):
            if c.isnumeric():
                current_number.append(c)
                current_positions.append((i, j))
            if not c.isnumeric():
                #If any numbers or positions are buffered - Create Number
                if current_number:
                    numbers.add(Number(
                        positions=tuple(current_positions), 
                        value=int("".join(current_number))
                    ))
                current_number = []
                current_positions = []
        else:
            #End of line
            if current_number:
                    numbers.add(Number(
                        positions=tuple(current_positions), 
                        value=int("".join(current_number))
                    ))
            current_number = []
            current_positions = []
                                         
    return symbols, numbers

def get_first_solution() -> int:
    symbols, numbers = parse_inpt()

    number_sum = 0

    for number in numbers:
        for symbol in symbols:
            if number.is_adjacent(symbol):
                number_sum += number.value
                break

    return number_sum


def get_second_solution() -> int:
    symbols, numbers = parse_inpt()

    ratio_sum = 0

    for symbol in symbols:
        if symbol.value == "*":
            adjacent = symbol.get_adjacent(numbers)
            if len(adjacent)==2:
                gear_ratio = 1
                for number in adjacent:
                    gear_ratio *= number.value
                
                ratio_sum += gear_ratio

    return ratio_sum


print(get_first_solution())
print(get_second_solution())
