import os.path as osp
from collections import Counter


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


ranking = {
    "five_of_a_kind": 7,
    "four_of_a_kind": 6,
    "full_house": 5,
    "three_of_a_kind": 4,
    "two_pair": 3,
    "one_pair": 2,
    "high_card": 1,
}


# part 1
values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}


class Hand:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = int(bid)
        self.type = self._assess_type()

    def _assess_type(self):
        c = Counter(self.hand)
        if len(c) == 1:
            return ranking["five_of_a_kind"]
        if len(c) == 2:
            if 4 in c.values():
                return ranking["four_of_a_kind"]
            return ranking["full_house"]
        if len(c) == 3:
            if 3 in c.values():
                return ranking["three_of_a_kind"]
            return ranking["two_pair"]
        if len(c) == 4:
            return ranking["one_pair"]
        return ranking["high_card"]

    def __lt__(self, other):
        if self.type == other.type:
            for c1, c2 in zip(self.hand, other.hand):
                if c1 == c2:
                    continue
                return int(values.get(c1, c1)) < int(values.get(c2, c2))

        return self.type < other.type


hands = []

for line in inp:
    hands.append(Hand(*line.split()))


winnings = 0
for idx, hand in enumerate(sorted(hands)):
    winnings += hand.bid * (idx + 1)
print(winnings)


# part 2
values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
}


class JokerHand(Hand):
    def _assess_type(self):
        if "J" not in self.hand:
            return super()._assess_type()
        return self._assess_joker_type()

    def _assess_joker_type(self):
        c = Counter(self.hand)
        mapping = {v: k for k, v in c.items()}
        if 5 in c.values():
            return ranking["five_of_a_kind"]
        if 4 in c.values():
            return ranking["five_of_a_kind"]
        if 3 in c.values():
            if 2 in c.values():
                return ranking["five_of_a_kind"]
            return ranking["four_of_a_kind"]
        if [1, 2, 2] == sorted(c.values()):
            if c["J"] == 1:
                return ranking["full_house"]
            return ranking["four_of_a_kind"]
        if 2 in c.values():
            return ranking["three_of_a_kind"]
        return ranking["one_pair"]


hands = []

for line in inp:
    hands.append(JokerHand(*line.split()))


winnings = 0
for idx, hand in enumerate(sorted(hands)):
    winnings += hand.bid * (idx + 1)
print(winnings)
