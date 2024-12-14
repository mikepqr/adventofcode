from collections import defaultdict

import aoc202412data

test = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".splitlines()

test2 = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""".splitlines()

test3 = """\
BA
AB""".splitlines()

# map = test
map = aoc202412data.data

NX = len(map[0])
NY = len(map)

DIRECTIONS = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
)


def region_cost(region: set[tuple[int, int]]) -> int:
    area = len(region)
    perimeter = 0
    for plot in region:
        for dx, dy in DIRECTIONS:
            if (plot[0] + dx, plot[1] + dy) not in region:
                perimeter += 1
    return area * perimeter


def explore(x, y, seen=None) -> set:
    if seen is None:
        seen = set()

    if (x, y) in seen:
        return seen

    seen.add((x, y))

    for dx, dy in DIRECTIONS:
        if 0 <= x + dx < NX and 0 <= y + dy < NY and map[y][x] == map[y + dy][x + dx]:
            explore(x + dx, y + dy, seen)

    return seen


def regions():
    found = set()
    for y, line in enumerate(map):
        for x, _ in enumerate(line):
            if (x, y) not in found:
                region = explore(x, y)
                found.update(region)
                yield region


def part1():
    return sum(region_cost(region) for region in regions())


def contiguous_sets(s: set) -> int:
    child2parent = {x: x for x in s}

    n = len(set(child2parent.values()))

    while True:
        for x in child2parent:
            if x - 1 in child2parent:
                child2parent[x - 1] = child2parent[x]
                for c, p in child2parent.items():
                    if p == x - 1:
                        child2parent[c] = x
            if x + 1 in child2parent:
                child2parent[x + 1] = child2parent[x]
                for c, p in child2parent.items():
                    if p == x + 1:
                        child2parent[c] = x
        n_ = len(set(child2parent.values()))
        if n == n_:
            return n
        else:
            n = n_


def count_edges(region):
    hedges = defaultdict(set)
    vedges = defaultdict(set)

    for plot in region:
        for dx, dy in DIRECTIONS:
            if (plot[0] + dx, plot[1] + dy) not in region:
                if dy:
                    hedges[(plot[1], dy)].add(plot[0])
                if dx:
                    vedges[(plot[0], dx)].add(plot[1])

    nedges = sum(
        contiguous_sets(edge) for edge in list(hedges.values()) + list(vedges.values())
    )

    return nedges


def part2():
    cost = 0
    for region in regions():
        cost += count_edges(region) * len(region)
    print(cost)
