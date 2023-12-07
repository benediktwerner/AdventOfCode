#!/usr/bin/env python3

from os import path
from collections import Counter
from typing import Callable, Iterator
import itertools

CARD_STRENGTHS = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
VALUES = list(map(str, range(2, 10))) + ["T", "Q", "K", "A"]
(
    HIGH_CARD,
    PAIR,
    TWO_PAIR,
    THREE_OF_A_KIND,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    FIVE_OF_A_KIND,
) = range(7)


def possible_unjokered_hands(hand: str) -> Iterator[str]:
    jokers = [i for i, c in enumerate(hand) if c == "J"]
    for replacements in itertools.product(VALUES, repeat=len(jokers)):
        for i, pos in enumerate(jokers):
            hand = hand[:pos] + replacements[i] + hand[pos + 1 :]
        yield hand


def hand_rank(hand: str) -> int:
    counts = [c[1] for c in Counter(hand).most_common()]
    if counts[0] == 5:
        return FIVE_OF_A_KIND
    if counts[0] == 4:
        return FOUR_OF_A_KIND
    if counts[0] == 3:
        if counts[1] == 2:
            return FULL_HOUSE
        return THREE_OF_A_KIND
    if counts[0] == 2:
        if counts[1] == 2:
            return TWO_PAIR
        return PAIR
    return HIGH_CARD


def joker_hand_rank(hand: str) -> int:
    return sorted(map(hand_rank, possible_unjokered_hands(hand)))[-1]


def card_value(card: str) -> int:
    if card in CARD_STRENGTHS:
        return CARD_STRENGTHS[card]
    return int(card)


def joker_card_value(card: str) -> int:
    return 0 if card == "J" else card_value(card)


def solve(hands, rank_fn: Callable[[str], int], tiebreaker_fn) -> int:
    hands = [
        (rank_fn(hand), tuple(map(tiebreaker_fn, hand)), bid) for hand, bid in hands
    ]
    return sum(bid * (i + 1) for i, (_, _, bid) in enumerate(sorted(hands)))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    hands = [(hand, int(bid)) for hand, bid in map(str.split, f.read().splitlines())]
    print("Part 1:", solve(hands, hand_rank, card_value))
    print("Part 2:", solve(hands, joker_hand_rank, joker_card_value))
