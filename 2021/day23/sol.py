#!/usr/bin/env python3

from os import path
from dataclasses import dataclass
import heapq


A, B, C, D = range(4)
EXIT = (2, 4, 6, 8)


@dataclass(frozen=True)
class State:
    energy: int
    rooms: tuple
    hallway: tuple = (None,) * 11

    def __lt__(self, other):
        return self.energy < other.energy

    @property
    def fingerprint(self):
        return (self.hallway, self.rooms)

    @property
    def is_done(self):
        return all(h is None for h in self.hallway) and all(
            all(a == i for a in room) for i, room in enumerate(self.rooms)
        )


def insert(tpl, i, new):
    return tpl[:i] + (new,) + tpl[i + 1 :]


def solve(rooms):
    room_size = len(rooms[0])
    todo = [State(0, rooms)]
    visited = set()
    while todo:
        state = heapq.heappop(todo)
        if state.is_done:
            return state.energy
        if state.fingerprint in visited:
            continue
        visited.add(state.fingerprint)
        for ri, room in enumerate(state.rooms):
            if room and not all(a == ri for a in room):
                a = room[-1]
                for to, d in ((-1, -1), (11, 1)):
                    for hi in range(EXIT[ri] + d, to, d):
                        if hi in EXIT:
                            continue
                        if state.hallway[hi] is not None:
                            break
                        new = State(
                            state.energy
                            + (room_size - len(room) + 1 + abs(EXIT[ri] - hi))
                            * (10 ** a),
                            insert(state.rooms, ri, room[:-1]),
                            insert(state.hallway, hi, a),
                        )
                        if new.fingerprint not in visited:
                            heapq.heappush(todo, new)
        for i, a in enumerate(state.hallway):
            if a is None:
                continue
            if i < EXIT[a] and any(
                u is not None for u in state.hallway[i + 1 : EXIT[a]]
            ):
                continue
            if i > EXIT[a] and any(
                u is not None for u in state.hallway[EXIT[a] + 1 : i]
            ):
                continue
            if any(u != a for u in state.rooms[a]):
                continue
            new = State(
                state.energy
                + (room_size - len(state.rooms[a]) + abs(EXIT[a] - i)) * (10 ** a),
                insert(state.rooms, a, (state.rooms[a] + (a,))),
                insert(state.hallway, i, None),
            )
            if new.fingerprint not in visited:
                heapq.heappush(todo, new)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    rooms = tuple(
        (ord(lines[3][2 * i + 3]) - ord("A"), ord(lines[2][2 * i + 3]) - ord("A"),)
        for i in range(4)
    )
    print(rooms)
    print("Part 1:", solve(rooms))
    rooms = (
        (rooms[0][0], D, D, rooms[0][1]),
        (rooms[1][0], B, C, rooms[1][1]),
        (rooms[2][0], A, B, rooms[2][1]),
        (rooms[3][0], C, A, rooms[3][1]),
    )
    print("Part 2:", solve(rooms))
