import os.path as osp


with open(osp.join(osp.dirname(__file__), "input.txt")) as fh:
    inp = fh.read().splitlines()


mapping = {
    "|": ((0, -1), (0, 1)),
    "-": ((-1, 0), (1, 0)),
    "L": ((0, -1), (1, 0)),
    "J": ((0, -1), (-1, 0)),
    "7": ((0, 1), (-1, 0)),
    "F": ((0, 1), (1, 0)),
}


nodes = {}
grid = {}


def get_node(coords, sign):
    if coords in nodes:
        return nodes[coords]
    node = Node(coords, sign)
    nodes[coords] = node
    return node


class Node:
    def __init__(self, coords, sign=None):
        self.coords = coords
        self.from_node = None
        self.to_node = None
        self._sign = sign
        self.is_outside = None

    def __repr__(self):
        if self.from_node is None:
            return f"{self.coords}: {self.sign}"
        return (
            f"{self.from_node.coords} -> {self.coords} -> {self.to_node.coords}"
        )

    @property
    def sign(self):
        if self._sign == "S":
            reference = set((self.from_node.coords, self.to_node.coords))
            if reference == set([self.up.coords, self.down.coords]):
                return "|"
            if reference == set([self.left.coords, self.right.coords]):
                return "-"
            if reference == set([self.up.coords, self.right.coords]):
                return "L"
            if reference == set([self.up.coords, self.left.coords]):
                return "J"
            if reference == set([self.left.coords, self.down.coords]):
                return "7"
            if reference == set([self.right.coords, self.down.coords]):
                return "F"
        return self._sign

    def connect(self):
        self.is_outside = True
        x, y = self.coords
        for nx, ny in mapping[self.sign]:
            coords = (x + nx, y + ny)
            if self.from_node.coords != coords:
                node = get_node(coords, grid[coords])
                self.to_node = node
                node.from_node = self

    @property
    def is_loop(self):
        return self.from_node is not None

    def neighbours(self):
        return [
            self.left,
            self.right,
            self.up,
            self.down,
        ]

    @property
    def left(self):
        return self._get_neighbour(-1, 0)

    @property
    def right(self):
        return self._get_neighbour(1, 0)

    @property
    def up(self):
        return self._get_neighbour(0, -1)

    @property
    def down(self):
        return self._get_neighbour(0, 1)

    def _get_neighbour(self, x_offset, y_offset):
        x, y = self.coords
        coords = (x + x_offset, y + y_offset)
        if coords not in grid:
            return
        return get_node(coords, grid[coords])


# populate raw grid
start = None
for y, line in enumerate(inp):
    for x, node in enumerate(line):
        grid[(x, y)] = node
        if node == "S":
            start = get_node((x, y), node)


# assess the sign of start and hook them up to its connections
for nx, ny in ((0, -1), (1, 0), (0, 1), (-1, 0)):
    x, y = start.coords
    nx, ny = (x + nx, y + ny)
    node = grid[(nx, ny)]
    if neighbours := mapping.get(node):
        for cx, cy in neighbours:
            if start.coords == (nx + cx, ny + cy):
                if start.from_node is None:
                    node = get_node((nx, ny), node)
                    start.from_node = node
                    node.to_node = start
                else:
                    node = get_node((nx, ny), node)
                    start.to_node = node
                    node.from_node = start

# Connect the entire loop nodes
position = start.to_node
while position.to_node is None:
    position.connect()
    position = position.to_node


# part 1
found = False
visited = []
dir1, dir2 = start.from_node, start.to_node
steps = 0

# move in both directions and stop when we meet each other
while not found:
    steps += 1
    visited.append(dir1.coords)
    dir1 = dir1.from_node

    if dir2.coords in visited:
        found = True
    visited.append(dir2.coords)
    dir2 = dir2.to_node

print(steps)


# part 2

# One side of the loop will always be outside, one side of the loop will always
# be inside. We first need to assess which side is the outside. We'll take
# (0, 0) and assume it is outside
node = get_node((0, 0), grid[(0, 0)])
if node.is_loop:
    raise ValueError("Wrong assumption dude")

# Travel to the right until we bump into the loop, and set every traveled node
# as outside while we're at it. If we go outside the grid, we go down 1,
# and repeat until we bump into the loop
previous_node = None
while not node.is_loop:
    node.is_outside = True
    x, y = node.coords
    previous_node = node
    if (x + 1, y) not in grid:
        node = get_node((0, y + 1), grid[(0, y + 1)])
    else:
        node = get_node((x + 1, y), grid[(x + 1, y)])

# We found the part of the loop we bumped into. Because we already set the
# nodes to "outside" while traveling, we know that all unset nodes are "inside"
for neighbour in node.neighbours():
    if neighbour.is_loop or neighbour.is_outside:
        continue
    neighbour.is_outside = False

# Based on the previous node, we can deduct what sides of this node is inside or
# outside, so we'll travel around the loop, step by step, setting the current
# node, based on the previous node
start = node
previous_node = node
node = start.to_node


# This config will tell us what sides are outside and what sides are inside
# based on the given scenarios. The top level key is the node we're currently
# enriching, the second level keys is what we have to do if the previous node
# was of the given type
#
# ("left", "left"), ("right", "right")
#
# is equivalent to
#
# node.left.is_outside = previous_node.left.is_outside
# node.right.is_outside = previous_node.right.is_outside
#
# "not right" translates to
# node.right.is_outside = not previous_node.right.is_outside
omapping = {
    "|": {
        "|": (("left", "left"), ("right", "right")),
        "F": (("left", "left"), ("right", "not left")),
        "7": (("right", "right"), ("left", "not right")),
        "L": (("left", "left"), ("right", "not left")),
        "J": (("right", "right"), ("left", "not right")),
    },
    "-": {
        "-": (("up", "up"), ("down", "down")),
        "F": (("up", "up"), ("down", "not up")),
        "7": (("up", "up"), ("down", "not up")),
        "L": (("down", "down"), ("up", "not down")),
        "J": (("down", "down"), ("up", "not down")),
    },
    "L": {
        "-": (("down", "down"), ("left", "down")),
        "|": (("left", "left"), ("down", "left")),
        "F": (("left", "left"), ("down", "left")),
        "7": (("left", "not right"), ("down", "not right")),
        "J": (("down", "down"), ("left", "down")),
    },
    "J": {
        "-": (("down", "down"), ("right", "down")),
        "|": (("right", "right"), ("down", "right")),
        "F": (("right", "not left"), ("down", "not left")),
        "7": (("right", "right"), ("down", "right")),
        "L": (("down", "down"), ("right", "down")),
    },
    "7": {
        "-": (("up", "up"), ("right", "up")),
        "|": (("right", "right"), ("up", "right")),
        "F": (("up", "up"), ("right", "up")),
        "J": (("right", "right"), ("up", "right")),
        "L": (("up", "not down"), ("right", "not down")),
    },
    "F": {
        "-": (("up", "up"), ("left", "up")),
        "|": (("left", "left"), ("up", "left")),
        "7": (("up", "up"), ("left", "up")),
        "J": (("up", "not down"), ("left", "not down")),
        "L": (("left", "left"), ("up", "down")),
    },
}


# Apply the above config while traveling around the loop
while node is not start:
    config = omapping.get(node.sign)
    if config:
        instructions = config[previous_node.sign]
        for set_attr, get_attr in config[previous_node.sign]:
            value = None
            if get_attr.startswith("not"):
                get_attr = get_attr.replace("not ", "")
                nnode = getattr(previous_node, get_attr)
                if nnode:
                    value = nnode.is_outside
                    if value is not None:
                        value = not value
                else:
                    value = True
            else:
                nnode = getattr(previous_node, get_attr)
                if nnode:
                    value = nnode.is_outside
                else:
                    value = True
            if value is not None:
                nnode = getattr(node, set_attr)
                if nnode:
                    nnode.is_outside = value
    previous_node = node
    node = node.to_node


def find_marked_node(node):
    if node.is_outside is not None:
        return node.is_outside
    else:
        if node.right is None:
            node.is_outside = True
        else:
            node.is_outside = find_marked_node(node.right)
        return node.is_outside


# Complete nodes that don't have their "is_outside" set. We'll take the node,
# travel to the right until we encounter a node that is set
# (or are outside the grid, in which case we'll know we're outside), and set its
# value to all nodes traveled. Then we do the same with the next unset node
# until there are no more unset nodes left
for y, line in enumerate(inp):
    for x, node in enumerate(line):
        node = get_node((x, y), node)
        if node.is_outside is None:
            find_marked_node(node)

# finally we count all nodes that are set as "inside"
print(len([n for n in nodes.values() if not n.is_loop and not n.is_outside]))
