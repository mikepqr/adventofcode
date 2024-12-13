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
