from utils import read_input
from abc import ABC, abstractmethod
from typing import Literal, TypeAlias
from collections import deque
import math

PulseType: TypeAlias = Literal[1, 0]
SignalType: TypeAlias = tuple[str, str, PulseType]


class Module(ABC):
    name: str
    output_modules: list[str]
    state: Literal[0, 1]

    def __init__(
        self,
        name: str,
        output_modules: list[str],
    ) -> None:
        self.name = name
        self.state = 0
        self.output_modules = output_modules

    @abstractmethod
    def on_signal(self, signal: SignalType) -> list[SignalType]:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.name}', state: {self.state})"


class FlipFlop(Module):
    def on_signal(self, signal: SignalType) -> list[SignalType]:
        if signal[2] == 1:
            return []
        else:
            if self.state == 1:
                self.state = 0
                return [(self.name, target, 0) for target in self.output_modules]
            else:
                self.state = 1
                return [(self.name, target, 1) for target in self.output_modules]


class Conjunction(Module):
    input_modules: dict[str, Literal[0, 1]]

    def __init__(
        self,
        name: str,
        output_modules: list[str],
        input_modules: list[str] | None = None,
    ) -> None:
        if input_modules:
            self.input_modules = {name: 0 for name in input_modules}

        return super().__init__(name, output_modules)

    def set_input_modules(self, input_modules: list[str]) -> None:
        self.input_modules = {name: 0 for name in input_modules}

    def on_signal(self, signal: SignalType) -> list[SignalType]:
        self.input_modules[signal[0]] = signal[2]
        if all(self.input_modules.values()):
            return [(self.name, target, 0) for target in self.output_modules]
        else:
            return [(self.name, target, 1) for target in self.output_modules]


def parse_input() -> tuple[dict[str, Module], list[SignalType]]:
    inpt = read_input("20")

    modules: dict[str, Module] = {}

    for row in inpt:
        if "broadcast" not in row:
            name = row.split("->")[0].strip("% " if "%" in row else "& ")
            output_modules = [name.strip(" ") for name in row.split("->")[1].split(",")]

            if "&" in row:
                modules[name] = Conjunction(name, output_modules)
            else:
                modules[name] = FlipFlop(name, output_modules)

    for module in modules.values():
        if type(module) == Conjunction:
            name = module.name
            input_modules = []
            for row in inpt:
                if name in row.split("->")[1]:
                    input_modules.append(row.split("->")[0].strip(" %&"))
            module.set_input_modules(input_modules)

    initial_output_modules: list[str] = []
    for row in inpt:
        if "broadcaster" in row:
            initial_output_modules = [
                name.strip(" ") for name in row.split("->")[1].split(",")
            ]
            break

    initial_output: list[SignalType] = [
        ("broadcaster", name, 0) for name in initial_output_modules
    ]

    return modules, initial_output


def press_button(
    modules: dict[str, Module], initial_output: list[SignalType]
) -> tuple[int, int]:
    signal_queue: deque[SignalType] = deque(initial_output)

    lows, highs = 1, 0

    while signal_queue:
        signal = signal_queue.popleft()
        target = signal[1]
        if target in modules.keys():
            for response_signal in modules[target].on_signal(signal):
                signal_queue.append(response_signal)
        if signal[2]:
            highs += 1
        else:
            lows += 1

    return lows, highs


def press_button_p2(
    modules: dict[str, Module], initial_output: list[SignalType], from_module: str
) -> bool:
    signal_queue: deque[SignalType] = deque(initial_output)

    while signal_queue:
        signal = signal_queue.popleft()
        target = signal[1]
        if target in modules.keys():
            for response_signal in modules[target].on_signal(signal):
                signal_queue.append(response_signal)

        if signal[0] == from_module and signal[2]:
            return True

    return False


def find_on(module_name: str) -> int:
    modules, initial_output = parse_input()

    for i in range(10**6):
        if press_button_p2(modules, initial_output, module_name):
            return i + 1

    return -1


def get_first_solution():
    modules, initial_output = parse_input()
    highs, lows = 0, 0

    for _ in range(1000):
        h, l = press_button(modules, initial_output)
        highs += h
        lows += l

    return highs * lows


def get_second_solution():
    modules, initial_output = parse_input()

    modules_to_find = ["hp"]

    modules_to_find_tmp = []
    for module in modules_to_find:
        if type(modules[module]) == Conjunction:
            modules_to_find_tmp += list(modules[module].input_modules.keys())
        else:
            modules_to_find_tmp += [module]

    modules_to_find = modules_to_find_tmp

    o = [find_on(module_name) for module_name in modules_to_find]

    return math.lcm(*o)


print(get_first_solution())
print(get_second_solution())
