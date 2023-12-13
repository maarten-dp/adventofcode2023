import os.path as osp


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().split("\n\n")


# Part 1
def is_reflection(lines, index):
    return all(
        [t1 == t2 for t1, t2 in zip(reversed(lines[:index]), lines[index:])]
    )


def find_reflection(lines):
    previous_line = None
    for idx, line in enumerate(lines):
        if line == previous_line:
            if is_reflection(lines, idx):
                return idx
        previous_line = line


summary = 0
for field in inp:
    lines = field.splitlines()
    if not (amount := find_reflection(lines)):
        summary += find_reflection(list(zip(*lines)))
    else:
        summary += amount * 100

print(summary)


# Part 2
def is_reflection(lines, index):
    had_smudges = False
    for t1, t2 in zip(reversed(lines[:index]), lines[index:]):
        if t1 == t2:
            continue
        had_smudges = True
        smudges = 0
        for c1, c2 in zip(t1, t2):
            if c1 != c2:
                smudges += 1
        if smudges > 1:
            return False
    return had_smudges


def find_reflection(lines):
    previous_line = None
    for idx, line in enumerate(lines):
        if is_reflection(lines, idx):
            return idx
        previous_line = line


summary = 0
for field in inp:
    lines = field.splitlines()
    if not (amount := find_reflection(lines)):
        summary += find_reflection(list(zip(*lines)))
    else:
        summary += amount * 100

print(summary)
