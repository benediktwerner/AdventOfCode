#!/usr/bin/env python3

import os
from collections import defaultdict


def main():
    points = defaultdict(int)

    for day in os.listdir("days"):
        with open(os.path.join("days", day)) as f:
            content = f.read()
            start = content.find(
                '<p>First hundred users to get <span class="leaderboard-daydesc-both">both stars</span>')
            middle = content.find(
                '<p>First hundred users to get the <span class="leaderboard-daydesc-first">first star</span>')
            end = content.find('</main>')

            first = content[start:middle].split("\n")
            second = content[middle:end].split("\n")[:-1]

            for i, line in enumerate(first):
                start = line.rfind("anonymous user")
                if start != -1:
                    end = line.find(")", start)
                else:
                    start = line.rfind("</span>") + len("</span>")
                    end = line.find("<", start)
                name = line[start:end]
                points[name] += 100 - i

            for i, line in enumerate(second):
                start = line.rfind("anonymous user")
                if start != -1:
                    end = line.find(")", start)
                else:
                    start = line.rfind("</span>") + len("</span>")
                    end = line.find("<", start)
                name = line[start:end]
                points[name] += 100 - i
    

    for i, name in enumerate(sorted(points, key=lambda n: -points[n])):
        print("Rank {}: {} with {} points".format(i+1, name, points[name]))


if __name__ == "__main__":
    main()
