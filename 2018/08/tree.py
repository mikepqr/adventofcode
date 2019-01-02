class Node():

    def __init__(self, metadata=None, children=None):
        self.metadata = metadata or []
        self.children = children or []

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child

    def __repr__(self):
        return 'Node(metadata={!r}, children={!r})'.format(self.metadata, self.children)

    def total_metatadata(self):
        return sum(m for descendent in self for m in descendent.metadata)

    def value(self):
        if self.children:
            return sum(
                self.children[m-1].value() for m in self.metadata
                if 0 < m <= len(self.children)
            )
        else:
            return sum(self.metadata)


def parse_node(data):
    """
    Return (Node, remaining data). Recurses until no remaining data, i.e.
    returns (Node, []).
    """
    n_children = data[0]
    n_metadata = data[1]
    data = data[2:]
    children = []
    for i in range(n_children):
        child, data = parse_node(data)
        children.append(child)
    metadata, data = data[:n_metadata], data[n_metadata:]
    return Node(metadata, children=children), data


def parse_input():
    with open("input.txt") as f:
        data = list(map(int, f.read().split()))
    return parse_node(data)[0]


def part1():
    tree = parse_input()
    return tree.total_metatadata()


def part2():
    tree = parse_input()
    return tree.value()
