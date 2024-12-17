from dataclasses import dataclass
from enum import Enum
from typing import Self

import aoc202416data
import dijkstra


class Direction(Enum):
    LEFT = -1, 0
    UP = 0, -1
    RIGHT = 1, 0
    DOWN = 0, 1

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    @property
    def ccw(self) -> Self:
        return self.__class__((-self.dy, self.dx))

    @property
    def cw(self) -> Self:
        return self.__class__((self.dy, -self.dx))


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Direction) -> Self:
        return self.__class__(self.x + other.dx, self.y + other.dy)


@dataclass(frozen=True)
class State:
    p: Point
    d: Direction


class Tile(Enum):
    WALL = "#"
    EMPTY = "."
    START = "S"
    END = "E"


class Map:

    def __init__(self, data: str):
        self._grid: dict[Point, Tile] = {
            Point(x, y): Tile(c)
            for y, line in enumerate(data.splitlines())
            for x, c in enumerate(line)
        }

    def __getitem__(self, p: Point | State) -> Tile:
        if isinstance(p, Point):
            return self._grid[p]
        else:
            return self._grid[p.p]

    def edges(self, state: State) -> set[tuple[int, State]]:
        destinations = set()
        if self[state.p + state.d] != Tile.WALL:
            destinations.add((1, State(state.p + state.d, state.d)))
        destinations.add((1000, State(state.p, state.d.cw)))
        destinations.add((1000, State(state.p, state.d.ccw)))
        return destinations

    @property
    def start(self) -> Point:
        return self._find(Tile.START)

    @property
    def end(self) -> Point:
        return self._find(Tile.END)

    def _find(self, tile: Tile) -> Point:
        return next(p for p, t in self._grid.items() if t == tile)


data = aoc202416data.data


def main() -> tuple[int | None, int]:
    map = Map(data)
    distance, paths = dijkstra.dijkstra_all_paths(
        State(map.start, Direction.RIGHT),
        # trial and error, I know the final state reaches E facing right.
        State(map.end, Direction.RIGHT),
        map.edges,
    )
    return distance, len({state.p for path in paths for state in path})
