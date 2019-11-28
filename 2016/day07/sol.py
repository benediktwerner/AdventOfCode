#!/usr/bin/env python3


def main():
    with open("input.txt") as f:
        count = 0

        for line in f:
            line = line.strip()

            inside = False
            found = False

            for i in range(len(line) - 3):
                if line[i] == "[":
                    inside = True
                elif line[i] == "]":
                    inside = False
                elif (
                    line[i + 1] not in ("[", "]")
                    and line[i] == line[i + 3] != line[i + 1] == line[i + 2]
                ):
                    if inside:
                        break
                    found = True
            else:
                if found:
                    count += 1

        print("Part 1:", count)

    with open("input.txt") as f:
        count = 0

        for line in f:
            line = line.strip()

            inside = False
            found_inside = set()
            found_outside = set()

            for i in range(len(line) - 2):
                if line[i] == "[":
                    inside = True
                elif line[i] == "]":
                    inside = False
                elif (
                    line[i + 1] not in ("[", "]")
                    and line[i] == line[i + 2] != line[i + 1]
                ):
                    if inside:
                        x = (line[i + 1], line[i])
                        if x in found_outside:
                            count += 1
                            break
                        found_inside.add(x)
                    else:
                        x = (line[i], line[i + 1])
                        if x in found_inside:
                            count += 1
                            break
                        found_outside.add(x)

        print("Part 2:", count)


if __name__ == "__main__":
    main()
