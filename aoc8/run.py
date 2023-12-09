import os.path as osp
from operator import itemgetter
from collections import defaultdict


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    raw_instructions, network = fh.read().split("\n\n")

# (
#     raw_instructions,
#     network,
# ) = """RL

# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)""".split(
#     "\n\n"
# )


# (
#     raw_instructions,
#     network,
# ) = """LLR

# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)""".split(
#     "\n\n"
# )


instructions = []
for instruction in raw_instructions:
    if instruction == "L":
        instructions.append(itemgetter(0))
    else:
        instructions.append(itemgetter(1))


class InfiniteList(list):
    def __getitem__(self, index):
        index %= len(self)
        return list.__getitem__(self, index)


nodes = {}
for line in network.splitlines():
    node, directions = line.split(" = ")
    left, right = directions[1:-1].split(", ")

    nodes[node] = (left, right)


# part 1
current_position = "AAA"

step = 0
lst = InfiniteList(instructions)
while lst:
    instruction = lst[step]
    current_position = instruction(nodes[current_position])
    if current_position == "ZZZ":
        break
    step += 1

print(step + 1)

# part 2
step = 0
lst = InfiniteList(instructions)
current_positions = {n: [] for n in nodes if n.endswith("A")}
intervals = []

while current_positions:
    instruction = lst[step]
    next_positions = {}
    for pos, items in list(current_positions.items()):
        next_pos = instruction(nodes[pos])
        next_positions[next_pos] = items
        if next_pos.endswith("Z"):
            items.append(step)
        if len(items) == 2:
            interval1, interval2 = next_positions.pop(next_pos)
            intervals.append((interval1, interval2 - interval1))

    current_positions = next_positions

    step += 1

intervals = list(reversed(sorted(intervals, key=lambda i: i[1])))

step = 1
while True:
    reference_number = (intervals[0][1] * step) + intervals[0][0]

    sums = []
    for start, interval in intervals[1:]:
        sums.append((reference_number - start) % interval)

    if sum(sums) == 0:
        break
    step += 1

print(reference_number)
