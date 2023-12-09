import os.path as osp


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


# part 1
def parse_future_sequence(sequence):
    difference = []
    for start, end in zip(sequence[:-1], sequence[1:]):
        difference.append(end - start)
    if sum(difference) == 0:
        return 0
    else:
        addition = parse_future_sequence(difference)
        return difference[-1] + addition


sums = 0
for line in inp:
    sequence = list(map(int, line.split()))
    sums += sequence[-1] + parse_future_sequence(sequence)

print(sums)


# part 2
def parse_history_sequence(sequence):
    difference = []
    for start, end in zip(sequence[:-1], sequence[1:]):
        difference.append(end - start)
    if sum(difference) == 0:
        return 0
    else:
        addition = parse_history_sequence(difference)
        return difference[0] - addition


sums = 0
for line in inp:
    sequence = list(map(int, line.split()))
    sums += sequence[0] - parse_history_sequence(sequence)
print(sums)
