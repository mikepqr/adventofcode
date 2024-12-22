from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Generator, Self

import aoc202420data


@dataclass(frozen=True)
class Move:
    dx: int
    dy: int

    def __add__(self, other: Self):
        return Point(self.dx + other.dx, self.dy + other.dy)

    def __len__(self) -> int:
        return abs(self.dx) + abs(self.dy)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Move):
        return Point(self.x + other.dx, self.y + other.dy)


Walls = set[Point]
Boxes = set[Point]
Robot = Point
Route = list[Move]


class Tile(Enum):
    WALL = "#"
    START = "S"
    END = "E"
    EMPTY = " "
    SEEN = "."


DIRECTIONS = (
    Move(-1, 0),
    Move(0, -1),
    Move(1, 0),
    Move(0, 1),
)


class World:

    def __init__(self, data: str) -> None:
        self.walls = set()
        map = data.splitlines()
        for y, line in enumerate(map):
            for x, c in enumerate(line):
                if Tile(c) == Tile.WALL:
                    self.walls.add(Point(x, y))
                elif Tile(c) == Tile.START:
                    self.start = Point(x, y)
                elif Tile(c) == Tile.END:
                    self.end = Point(x, y)
        if self.start is None or self.end is None:
            raise ValueError

    @property
    def nx(self) -> int:
        if hasattr(self, "_nx"):
            return self._nx
        else:
            self._nx = max(w.x for w in self.walls)
            return self._nx

    @property
    def ny(self) -> int:
        if hasattr(self, "_ny"):
            return self._ny
        else:
            self._ny = max(w.y for w in self.walls)
            return self._ny

    def __contains__(self, p: Point) -> bool:
        if 0 <= p.x < self.nx and 0 <= p.y < self.ny:
            return True
        return False

    def __getitem__(self, p: Point) -> Tile:
        if p in self.walls:
            return Tile.WALL
        elif p == self.start:
            return Tile.START
        elif p == self.end:
            return Tile.END
        elif p in self:
            return Tile.EMPTY
        else:
            raise IndexError

    def draw(self, seen=None, cheats=None, curr=None) -> None:
        if seen is None:
            seen = set()
        if cheats is None:
            cheats = set()
        for y in range(self.ny + 1):
            for x in range(self.nx + 1):
                if Point(x, y) == curr:
                    print("*", end="")
                elif Point(x, y) in cheats:
                    print("1", end="")
                elif Point(x, y) in seen:
                    print("*", end="")
                else:
                    print(self[Point(x, y)].value, end="")

            print()

    def shortest(
        self,
    ) -> dict[Point, int]:
        """
        BFS to get the distance from self.start to each reachable point.
        """
        q = deque()
        q.append((0, self.start))
        times = {}
        while q:
            d, curr = q.popleft()
            if curr in times:
                continue
            times[curr] = d
            for move in DIRECTIONS:
                new = curr + move
                try:
                    if self[new] in {Tile.EMPTY, Tile.END}:
                        q.append((d + 1, new))
                except IndexError:
                    pass

        return times

    def shortest_with_cheats(
        self,
        cheat_duration: int = 2,
    ) -> dict[int, set[tuple[Point, Point]]]:

        total_time_no_cheats = self.shortest()
        time_to_beat = total_time_no_cheats[self.end]
        time_remaining_no_cheats = {
            curr: time_to_beat - t for curr, t in total_time_no_cheats.items()
        }

        cheats = defaultdict(set)

        for curr, t in total_time_no_cheats.items():
            for new, dt in self.reachable(curr, distance=cheat_duration):
                if new in time_remaining_no_cheats:
                    time_with_cheat = t + dt + time_remaining_no_cheats[new]
                    if time_with_cheat < time_to_beat:
                        cheats[time_to_beat - time_with_cheat].add((curr, new))

        return cheats

    def reachable(
        self, p: Point, distance: int = 2
    ) -> Generator[tuple[Point, int], None, None]:
        """
        Yield all points within a distance d of p that are not walls or the start.
        """
        for dx in range(-distance, distance + 1):
            for dy in range(-distance + abs(dx), distance + 1 - abs(dx)):
                if dx == dy == 0:
                    continue
                move = Move(dx, dy)
                new = p + move
                if new in self and self[new] in {Tile.EMPTY, Tile.END}:
                    yield new, len(move)


def part1():
    world = World(aoc202420data.data)
    cheats = world.shortest_with_cheats()
    return sum(len(v) for saving, v in cheats.items() if saving >= 100)


def part2():
    world = World(aoc202420data.data)
    cheats = world.shortest_with_cheats(cheat_duration=20)
    return sum(len(v) for saving, v in cheats.items() if saving >= 100)
