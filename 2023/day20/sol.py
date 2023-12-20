#!/usr/bin/env python3

from os import path
from collections import defaultdict, deque
import itertools
import math


class Broadcaster:
    def __init__(self, targets: list[str]):
        self.targets = targets

    def process(self, state: bool, origin: str):
        return state


class FlipFlop:
    def __init__(self, targets: list[str]):
        self.targets = targets
        self.state = 0

    def process(self, state: bool, origin: str):
        if not state:
            self.state = not self.state
            return self.state


class Conjunction:
    def __init__(self, targets: list[str]):
        self.targets = targets
        self.states = {}

    def process(self, state: bool, origin: str):
        self.states[origin] = state
        return not all(self.states.values())


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    modules, reverse = {}, defaultdict(list)
    for line in file.read().splitlines():
        mod, targets = line.split(" -> ")
        targets = targets.split(", ")
        mod_type, mod_name = mod[0], mod[1:]
        for t in targets:
            reverse[t].append("broadcaster" if mod_type == "b" else mod_name)
        match mod_type:
            case "b":
                modules["broadcaster"] = Broadcaster(targets)
            case "%":
                modules[mod_name] = FlipFlop(targets)
            case "&":
                modules[mod_name] = Conjunction(targets)
            case _:
                assert False

    for k, m in modules.items():
        if isinstance(m, Conjunction):
            for inp in reverse[k]:
                m.states[inp] = False

    final_and = reverse["rx"][0]
    counter_outputs = reverse[final_and]
    counter_outputs_cycle = {}

    pulses = [1000, 0]

    for i in itertools.count(1):
        todo = deque([("broadcaster", False, None)])
        while todo:
            target, state, origin = todo.popleft()
            module = modules[target]
            result = module.process(state, origin)
            if result is not None:
                if i <= 1000:
                    pulses[result] += len(module.targets)
                for t in module.targets:
                    if (
                        not result
                        and t in counter_outputs
                        and t not in counter_outputs_cycle
                    ):
                        counter_outputs_cycle[t] = i
                    if t in modules:
                        todo.append((t, result, target))
        if len(counter_outputs_cycle) == len(counter_outputs) and i >= 1000:
            break

    print("Part 1:", math.prod(pulses))
    print("Part 2:", math.lcm(*counter_outputs_cycle.values()))
