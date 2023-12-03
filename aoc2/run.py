import os.path as osp


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


from collections import defaultdict

required = {"red": 12, "green": 13, "blue": 14}

sum_possible_ids = 0

for line in inp:
    game, cubes = line.split(": ")
    game_id = game.split(" ")[-1]

    can_happen = True
    for shown in cubes.split("; "):
        for shown_cubes in shown.split(", "):
            amount, color = shown_cubes.split(" ")
            if required[color] < int(amount):
                can_happen = False
                break
        if not can_happen:
            break
    if can_happen:
        sum_possible_ids += int(game_id)

print(sum_possible_ids)


import operator as op
from functools import reduce

sum_powers = 0

for line in inp:
    all_shown_cubes = defaultdict(lambda: 0)

    game, cubes = line.split(": ")
    game_id = game.split(" ")[-1]

    can_happen = True
    for shown in cubes.split("; "):
        for shown_cubes in shown.split(", "):
            amount, color = shown_cubes.split(" ")
            all_shown_cubes[color] = max(all_shown_cubes[color], int(amount))
    sum_powers += reduce(op.mul, all_shown_cubes.values())

print(sum_powers)
