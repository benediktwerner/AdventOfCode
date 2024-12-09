#!/usr/bin/env python3

from copy import deepcopy
from dataclasses import dataclass
from os import path


@dataclass
class Block:
    id: int | None
    size: int


def compute_checksum(blocks: list[Block]) -> int:
    result = 0
    i = 0
    for b in blocks:
        if b.id is not None:
            for _ in range(b.size):
                result += i * b.id
                i += 1
        else:
            i += b.size
    return result


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    blocks = []
    next_free = False
    next_id = 0
    for size in map(int, file.read().strip()):
        if next_free:
            blocks.append(Block(None, size))
        else:
            blocks.append(Block(next_id, size))
            next_id += 1
        next_free = not next_free

    blocks2 = deepcopy(blocks)

    i = 0
    while i < len(blocks):
        if blocks[i].id is not None:
            i += 1
        elif blocks[-1].id is None:
            blocks.pop()
        elif blocks[i].size == blocks[-1].size:
            blocks[i] = blocks.pop()
            i += 1
        elif blocks[i].size > blocks[-1].size:
            b = blocks.pop()
            blocks.insert(i + 1, Block(None, blocks[i].size - b.size))
            blocks[i] = b
            i += 1
        else:
            blocks[i].id = blocks[-1].id
            blocks[-1].size -= blocks[i].size
            i += 1

    print("Part 1:", compute_checksum(blocks))

    blocks = blocks2

    for id in range(next_id - 1, -1, -1):
        for i, b in enumerate(blocks):
            if b.id == id:
                break
        for j, nb in enumerate(blocks):
            if j >= i:
                break
            if nb.id is None and nb.size >= b.size:
                blocks[j] = deepcopy(b)
                if nb.size > b.size:
                    blocks.insert(j + 1, Block(None, nb.size - b.size))
                    i += 1
                if i > 0 and blocks[i - 1].id is None:
                    blocks[i - 1].size += b.size
                    blocks.pop(i)
                    i -= 1
                else:
                    blocks[i].id = None
                if i < len(blocks) - 1 and blocks[i + 1].id is None:
                    blocks[i].size += blocks[i + 1].size
                    blocks.pop(i + 1)
                break

    print("Part 2:", compute_checksum(blocks))
