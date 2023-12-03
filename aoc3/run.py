import os.path as osp


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


neighbours = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]


class Number:
    def __init__(self):
        self.number = ""
        self.coordinates = []
        self._neighbours = None

    def append(self, part, coordinate):
        self.number = f"{self.number}{part}"
        self.coordinates.append(coordinate)

    def neighbours(self):
        if self._neighbours is None:
            self._neighbours = set()
            for x_offset, y_offset in neighbours:
                for x, y in self.coordinates:
                    coordinate = (x + x_offset, y + y_offset)
                    if coordinate not in self.coordinates:
                        self._neighbours.add(coordinate)
        return self._neighbours

    @property
    def value(self):
        return int(self.number)


grid = []
symbols = []
gears = []
numbers = []

for y, line in enumerate(inp):
    number = None
    for x, char in enumerate(line):
        coordinate = (x, y)
        if char.isnumeric():
            if number is None:
                number = Number()
                numbers.append(number)
            number.append(char, coordinate)
        else:
            number = None
            if char != ".":
                symbols.append(coordinate)
                if char == "*":
                    gears.append(coordinate)


parts_sum = 0
for number in numbers:
    if set(number.neighbours()).intersection(symbols):
        parts_sum += number.value

print(parts_sum)


gear_sum = 0
for gear in gears:
    connected_numbers = []
    for number in numbers:
        if gear in set(number.neighbours()):
            connected_numbers.append(number)

    if len(connected_numbers) == 2:
        n1, n2 = connected_numbers
        gear_sum += n1.value * n2.value

print(gear_sum)
