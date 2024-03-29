from dataclasses import dataclass
from itertools import combinations

data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".strip().splitlines()

data = """
................................................#.........#............................................#....................................
..#.............#......#.............................................#...........................................................#..........
..............................................................#..............................#..............................................
.................................................................................................................#..........................
...........#...........................#...............................................#..................................#.............#...
............................#..................#.....#..........................#...........................................................
..................................#................................#........................................................................
...........................................................................#................................................................
.....#...................................#......................................................#.......................#...........#.....#.
.....................#........#....................#....................................................#...................................
......................................................................#.....................................................................
...........................................................#.................................#..............................................
........#..................#....................#....................................................#......................................
#.............#....................................................#..............#.............................#...........................
...................#.............#...................................................................................#...............#......
.............................................................................#.............................................................#
.........................................................................................................#..................................
....#...........................................................................................#...........................#.....#.........
.....................#.......................#.........#....................................................................................
#............#.........................................................................#....................#...............................
................................#..................#...........#......#............................#...................#.......#............
.......................................................................................................................................#....
...................................................................................#........................................................
.........................#.............#...................................................................................#................
............................................................................................................................................
..........#..............................................................#......#.........#..........#......................................
............................................................................................................................................
.................................................................................................#............................#.............
................#...............................#............#.....................#........................................................
.#........................#..........................#......................................................#.......................#.......
.......#....................................#................................#..............................................................
.................................#.....................................#..................................................................#.
........................................................#.............................#...............................#........#............
.....................#...................#.....#...............#............................................................................
.............#...................................................................................................#..........................
................................................................................................#.....#...............................#.....
.................#................#................#........................................................................................
.#..........................#.............................#.......#.......#................................................................#
.............................................#.............................................................#................................
...........#.................................................................................#...............................#..............
.....................#.................................#.......#..................................................................#.....#...
.......#..............................#..............................................................#......................................
#...............................#.....................................#...............#........................#.......#....................
...........................................................................#.....#.........................................................#
...........................................................................................#................................................
........................................................#................................................#.......................#..........
.........#............#............................................#.................................................#.....#................
............................................................................................................................................
......................................#......#........................................................#.........#...........................
.............#.....#......#..........................#......................................................................................
......#................................................................................................................................#....
.............................................................................................................#..............................
..#.......#.............................#.....................#..................#........#.................................................
............................................................................................................................................
......................................................................................#...............................#.....................
..................#...........................#...........................#.........................#.........................#.............
............................................................................................................................................
......................................#..................................................#.........................................#........
.......................#.....#................................................................#.............#............#..................
.....#.............................................#.............#..........................................................................
.............#...........................................................#.......#..................................#...........#...........
.................................#..........................................................................................................
.............................................#...........#..................................................................................
.......#......................................................#............................#.........#........#.............................
.....................#................................................#...........................................................#.........
...............#...................#...............#.......................................................................#................
#..........................#......................................................................#.........................................
.............................................................................#..............................................................
...............................#......#.................#..............................................#..........#.........................
...........................................................................................................................................#
.................#......#.......................#....................................#.....#..............................#.................
.........#.............................................................#..................................#.................................
....................................................#............#............#.........................................................#...
..#.........................................................#........................................................#..........#...........
............................................................................................................................................
............................................................................................................................................
.......#...........................#..............................................................#.........................................
....................#...................................#................................................................#..................
..............................#.............................................................................................................
..#......................#.............................................#........#..........#................................................
..........#.............................#......................#................................................................#...........
.....................................................................................................#......................................
......................#.............................................................................................#......................#
#................#..................................#........................................#.................#............................
...................................#......#.......................#...........#..........................................#.............#....
............................................................................................................................................
..........#..............................................#..................................................................................
............................................................................................................................................
....................#......#..........#.......................#......#....................#..........#.......#..................#...........
...#.........................................................................#..............................................................
..................................................................................#..............#..........................................
........#.......................#..........#................................................................................................
..............#...........................................................................................#.................................
................................................................#.......................................................................#...
.......................#................#.....................................................................#.............................
....#............#............#.................................................................#.....#.....................................
...................................................................................................................#........................
...........................................#..............................................................................#.................
.......#.........................................#.......#.......#.....#...............................................................#....
................................................................................#...........#.....................................#.........
...........#.....................................................................................#..........................................
..............................................................#.............................................................................
...............#.........#..........#........................................................................#..............................
...........................................#......................................................................#......#..................
....#...............#.......................................................................................................................
......................................................................................#..............................................#......
...............................................#...............#..............#.................#...........................................
.#.........................................................................................#.........................#......................
................#......#................#................................#..........................#...........#...........................
......#......................#.....................#.......#................................................................................
.............................................#...........................................................#...............#.....#........#...
...........#.........................................................................#......................................................
............................................................................#...............................................................
.........................................................................................#............................#.....................
...................#...................#.....................#....................................#.............#...........................
.................................#..........................................................................................................
.......#......#...........#..................................................................................................#.....#........
.......................................................................#..............#........#.............#..............................
......................#..................#......#..............#..............#.....................................#..................#....
..........................................................................................#.............#...................................
.........#..........................................#..............#.......................................................#................
.............................#..............................................................................................................
.............................................#...................................#..........................................................
................#..................#........................................#......................................#........................
....#.................#.................#.............................................#.................................#..................#
............................................................#.........#..................................#..................................
......................................................#...................................#.................................................
.................................#..................................................................#.......................................
.................................................#...................................................................................#......
............................................................................................................................................
..................#.............................................#.............#.........................#................#..................
.........#.................................................#...........#.............#........#..............#............................#.
...................................#.........................................................................................#..............
............................................................................................................................................
#.....................#...................................................#.......#...............................#.........................
..............................#.................#........#..........................................................................#.......
..............#........................................................................#....................................................
...........................................#.............................................................#..............................#...
.................................#...................................................................................#...........#..........
...........#.......#.......#...........................#.....#................#......................#........#.............................
""".strip().splitlines()


@dataclass
class Coord:
    x: int
    y: int

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class Vector:
    dx: int
    dy: int

    def __len__(self):
        return abs(self.dx) + abs(self.dy)


def transpose(data):
    new_data = []
    for x in range(len(data[0])):
        new_data.append("".join(line[x] for line in data))
    return new_data


def stretch(data):
    new_data = []
    for line in data:
        new_data.append(line)
        if all(c == "." for c in line):
            new_data.append("." * len(line))
    return new_data


def expand(data):
    data = stretch(data)
    data = transpose(data)
    data = stretch(data)
    data = transpose(data)
    return data


def find_galaxies(data):
    i = 1
    galaxies = {}
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == "#":
                galaxies[i] = Coord(x, y)
                i += 1
    return galaxies


def part1_naive():
    map = expand(data)
    galaxies = find_galaxies(map)
    pairs = list(combinations(galaxies, 2))
    distances = [len(galaxies[pair[0]] - galaxies[pair[1]]) for pair in pairs]
    return sum(distances)


def sum_expanded_distances(N):
    galaxies = find_galaxies(data)
    empty_rows = [i for i, row in enumerate(data) if all(c == "." for c in row)]
    empty_cols = [x for x in range(len(data[0])) if all(row[x] == "." for row in data)]
    pairs = list(combinations(galaxies, 2))
    distances = []
    for g1, g2 in pairs:
        c1, c2 = galaxies[g1], galaxies[g2]
        unexpanded_distance = len(c1 - c2)
        minx = min(c1.x, c2.x)
        maxx = max(c1.x, c2.x)
        miny = min(c1.y, c2.y)
        maxy = max(c1.y, c2.y)
        dy = len([y for y in empty_rows if miny < y < maxy]) * (N - 1)
        dx = len([x for x in empty_cols if minx < x < maxx]) * (N - 1)
        distances.append(unexpanded_distance + dx + dy)
    return sum(distances)


def part1():
    return sum_expanded_distances(N=2)


def part2():
    return sum_expanded_distances(N=1_000_000)


if __name__ == "__main__":
    print(part1())
    print(part2())
