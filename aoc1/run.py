import os.path as osp


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.readlines()


def get_simple_number(line):
    start = None
    end = None
    for char in line:
        if char.isnumeric():
            start = char
            break

    for char in reversed(line):
        if char.isnumeric():
            end = char
            break
    return int(f"{start}{end}")


digit_mapping = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_complex_number(line):
    start = None
    end = None

    while not start or not end:
        if start is None:
            for number in digit_mapping:
                if line.startswith(number):
                    start = digit_mapping[number]
                    break
                elif line[0].isnumeric():
                    start = line[0]
                    break
            if start is None:
                line = line[1:]
        if end is None:
            for number in digit_mapping:
                if line.endswith(number):
                    end = digit_mapping[number]
                    break
                elif line[-1].isnumeric():
                    end = line[-1]
                    break
            if end is None:
                line = line[:-1]

    return int(f"{start}{end}")


total = 0
complex_total = 0
for line in inp:
    if not line:
        continue
    total += get_simple_number(line)
    complex_total += get_complex_number(line)
print(total)
print(complex_total)
