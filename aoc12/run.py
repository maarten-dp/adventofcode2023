import os.path as osp
from collections import Counter
from itertools import product, chain
from functools import lru_cache

with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


# naive part one
arrangements = 0
for line in inp:
    arrangement, springs = line.split()
    springs = list(map(int, springs.split(",")))
    arrangement = arrangement.replace("?", "{}")
    for candidate in product([".", "#"], repeat=Counter(line)["?"]):
        groups = arrangement.format(*candidate).replace(".", " ").split()
        if [len(g) for g in groups] == springs:
            arrangements += 1

print(arrangements)


# painful part two
VALS = ["#", "."]


@lru_cache(maxsize=2000000)
def resolve_arrangement(arrangement, *springs):
    if not springs:
        return not arrangement or "#" not in arrangement
    if not arrangement:
        return 0

    template = arrangement.strip(".")
    spring_length = springs[0]
    arrangements = 0

    if "?" not in template:
        group = template.replace(".", " ").split()
        arrangements += tuple([len(g) for g in group]) == springs
    else:
        for val in VALS:
            arrangement = template.replace("?", val, 1)
            if arrangement.startswith("#" * spring_length):
                if len(arrangement) == spring_length:
                    if len(springs) == 1:
                        arrangements += 1
                elif arrangement[spring_length] in (".", "?"):
                    arrangement = arrangement[spring_length + 1 :]
                    arrangements += resolve_arrangement(
                        arrangement, *springs[1:]
                    )
            else:
                spring = arrangement[:spring_length]
                if spring.startswith("#") and "." in spring:
                    continue
                arrangements += resolve_arrangement(arrangement, *springs)
    return arrangements


arrangements = 0
for idx, line in enumerate(inp):
    print(f"{idx}/{len(inp)}")
    arrangement, springs = line.split()
    arrangement = "?".join([arrangement] * 5)
    springs = ",".join([springs] * 5)
    springs = list(map(int, springs.split(",")))

    arrangements += resolve_arrangement(arrangement, *springs)
print(arrangements)
