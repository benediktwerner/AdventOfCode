
from __future__ import print_function

def part1(components, total_strength=0, last_port=0):
    max_strength = total_strength
    max_bridge = []
    for c in components:
        a, b = c
        if a == last_port or b == last_port:
            if b == last_port:
                a, b = b, a
            components.remove(c)
            strength, bridge = part1(components, total_strength + a + b, b)
            if strength > max_strength:
                max_strength = strength
                max_bridge = bridge
                max_bridge.append("{}/{}".format(a, b))
            components.add(c)
    return max_strength, max_bridge

def part2(components, curr_length=0, last_port=0):
    max_length = curr_length
    max_bridge = []
    for c in components:
        a, b = c
        if a == last_port or b == last_port:
            if b == last_port:
                a, b = b, a
            components.remove(c)
            length, bridge = part2(components, curr_length + 1, b)
            if length > max_length:
                max_length = length
                max_bridge = bridge
                max_bridge.append("{}/{}".format(a, b))
            components.add(c)
    return max_length, max_bridge

def bridge_strength(bridge):
    return sum([sum(map(int, x.split("/"))) for x in bridge])

def main():
    components = set()
    with open("input.txt", "r") as f:
        for line in f:
            a, b = map(int, line.strip().split("/"))
            components.add((a, b))
    max_strength, bridge = part1(components)
    print("Max strength:", max_strength)
    print("With bridge:", "--".join(reversed(bridge)))
    
    length, bridge = part2(components)
    print("Length:", length)
    print("Strength:", bridge_strength(bridge))
    print("With bridge:", "--".join(reversed(bridge)))


if __name__ == "__main__":
    main()
