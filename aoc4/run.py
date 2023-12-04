import os.path as osp
from collections import defaultdict


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


total_points = 0
for line in inp:
    _, numbers = line.split(": ")
    winning_numbers, my_numbers = numbers.split(" | ")
    winning_numbers = set(map(int, winning_numbers.split()))
    my_numbers = set(map(int, my_numbers.split()))

    if my_winnning_numbers := winning_numbers.intersection(my_numbers):
        if len(my_winnning_numbers) == 1:
            total_points += 1
        else:
            total_points += 2 ** (len(my_winnning_numbers) - 1)

print(total_points)


cards = defaultdict(lambda: 0)

for line in inp:
    card, numbers = line.split(": ")
    card_number = int(card.split()[-1])
    cards[card_number] += 1

    winning_numbers, my_numbers = numbers.split(" | ")
    winning_numbers = set(map(int, winning_numbers.split()))
    my_numbers = set(map(int, my_numbers.split()))

    my_winnning_numbers = winning_numbers.intersection(my_numbers)

    end_range = card_number + len(my_winnning_numbers) + 1
    if end_range > len(inp):
        end_range = len(inp) + 1
    for number in range(card_number + 1, end_range):
        cards[number] += 1 * cards[card_number]

print(sum(cards.values()))
