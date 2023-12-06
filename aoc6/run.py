import os.path as osp
import operator as op
from functools import reduce

with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


times, distances = inp
times = map(int, times.split(": ")[-1].split())
distances = map(int, distances.split(": ")[-1].split())

combos = []
for time, record in zip(times, distances):
    winning_combinations = 0
    for push_time in range(time):
        travel_time = time - push_time
        if travel_time * push_time > record:
            winning_combinations += 1
    combos.append(winning_combinations)

print(reduce(op.mul, combos))


times, distances = inp
time = int("".join(times.split(": ")[-1].split()))
record = int("".join(distances.split(": ")[-1].split()))
winning_combinations = 0
for push_time in range(time):
    travel_time = time - push_time
    if travel_time * push_time > record:
        winning_combinations += 1
    if winning_combinations > 0 and travel_time * push_time < record:
        break
print(winning_combinations)
