import os.path as osp
from collections import defaultdict


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


class Range:
    def __init__(self, start, rng):
        self.start = start
        self.range = rng

    @property
    def end(self):
        return self.start + self.range - 1

    def __contains__(self, number):
        return self.start <= number <= self.end

    def __eq__(self, range):
        return self.start == range.start and self.range == range.range

    def index(self, number):
        if number in self:
            return number - self.start

    def get(self, index):
        if index is not None:
            return self.start + index

    def get_unique_ranges(self, range):
        if self == range:
            return [self]
        if not self.has_overlap(range):
            return [self, range]

        points = sorted(
            set([self.start, range.start, self.end + 1, range.end + 1])
        )
        ranges = []
        for start, end in zip(points[:-1], points[1:]):
            ranges.append(Range(start, end - start))
        return ranges

    def has_overlap(self, range):
        inside = range.start in self or range.end in self
        overlaps = range.start < self.start and self.end < range.end
        return inside or overlaps

    def __repr__(self):
        return f"{self.start} -> {self.end}"


class Map:
    def __init__(self, start_x, start_y, range):
        self.x = Range(start_x, range)
        self.y = Range(start_y, range)

    def __contains__(self, number):
        return number in self.range

    @property
    def range(self):
        return self.x

    def get(self, number):
        return self.y.get(self.x.index(number))

    def get_mapping(self, range):
        ranges = self.range.get_unique_ranges(range)
        relevant_range = None
        for unique_range in list(ranges):
            overlaps_with_self = unique_range.has_overlap(self.range)
            overlaps_with_range = unique_range.has_overlap(range)
            if overlaps_with_self and overlaps_with_range:
                index = self.x.index(unique_range.start)
                relevant_range = Range(self.y.start + index, unique_range.range)
                ranges.remove(unique_range)
            elif overlaps_with_self:
                ranges.remove(unique_range)

        return relevant_range, ranges

    def __lt__(self, other):
        return self.x.start < other.x.start

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return (
            f"{self.x.start}(+{self.x.range}) & {self.y.start}(+{self.x.range})"
        )


class Maps:
    def __init__(self, maps_to):
        self.mappings = []
        self.maps_to = maps_to

    def add_map(self, start_y, start_x, range):
        self.mappings.append(Map(start_x, start_y, range))

    def get(self, number):
        for mapping in self.mappings:
            if number in mapping:
                return mapping.get(number)
        return number

    def has_overlap(self, range):
        return any([m.range.has_overlap(range) for m in self.mappings])

    def get_range(self, ranges):
        self.mappings = sorted(self.mappings)

        mapped_ranges = []
        while ranges:
            range = ranges.pop()
            if not self.has_overlap(range):
                mapped_ranges.append(range)
                continue
            for mapping in self.mappings:
                if mapping.range.has_overlap(range):
                    mapped, unmapped = mapping.get_mapping(range)
                    if mapped is not None:
                        mapped_ranges.append(mapped)
                        ranges.extend(unmapped)
                        break

        return mapped_ranges

    def __repr__(self):
        return "\n----\n".join([str(m) for m in self.mappings])


MAPS = {}
SEEDS = []


for line in inp:
    if line.startswith("seeds"):
        SEEDS = list(map(int, line.replace("seeds: ", "").split()))
    elif line and line[0].isdigit():
        mapping.add_map(*map(int, line.split()))
    elif line:
        mapping_name, _ = line.split()
        name, maps_to = mapping_name.split("-to-")
        mapping = Maps(maps_to)
        MAPS[name] = mapping


# part 1
def get_value(number, mapping_name):
    maps_to = "seed"

    while maps_to != mapping_name:
        mapping = MAPS[maps_to]
        number = mapping.get(number)
        maps_to = mapping.maps_to
    return number


locations = []
for seed in SEEDS:
    locations.append((get_value(seed, "location")))

print(min(locations))


# part 2
def get_range_value(number, range, mapping_name):
    maps_to = "seed"
    ranges = [Range(number, range)]
    while maps_to != mapping_name:
        mapping = MAPS[maps_to]
        new_ranges = mapping.get_range(ranges)

        maps_to = mapping.maps_to
        ranges = new_ranges
    return ranges


import time

t1 = time.time()
location = float("inf")
for seed, rng in zip(SEEDS[::2], SEEDS[1::2]):
    lowest_location_for_seed = min(
        [s.start for s in get_range_value(seed, rng, "location")]
    )
    location = min([location, lowest_location_for_seed])

print(location)
print(time.time() - t1)
