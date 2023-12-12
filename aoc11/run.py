import os.path as osp
import time

with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()

galaxies = []
offset = 1000000

t1 = time.time()

# Find galaxy coordinates
for y, row in enumerate(inp):
    for x, sign in enumerate(row):
        if sign == "#":
            galaxies.append((x, y))


# Apply expansion rules
xes = sorted(set(g[0] for g in galaxies))
ys = sorted(set(g[1] for g in galaxies))

x_mapping = {}
y_mapping = {}


def get_expansion(d1, d2, expanded):
    difference = d2 - d1
    if expansion := (difference - 1) * offset:
        expanded += expansion - (difference - 1)
    return expanded


# expand x axis
expanded = 0
for x1, x2 in zip(xes[:-1], xes[1:]):
    expanded = get_expansion(x1, x2, expanded)
    x_mapping[x2] = expanded + x2


# expand y axis
expanded = 0
for y1, y2 in zip(ys[:-1], ys[1:]):
    expanded = get_expansion(y1, y2, expanded)
    y_mapping[y2] = expanded + y2


# Shift the galaxies wrt the expansion calculated above
expanded_galaxies = []
for x, y in galaxies:
    expanded_galaxies.append((x_mapping.get(x, x), y_mapping.get(y, y)))


# get the distance between galaxies
steps = 0
while expanded_galaxies:
    fgx, fgy = expanded_galaxies.pop()
    for tgx, tgy in expanded_galaxies:
        steps += abs(fgx - tgx) + abs(fgy - tgy)

print(steps)
print(time.time() - t1)
