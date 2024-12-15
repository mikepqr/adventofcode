from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Self

import aoc202415data


@dataclass(frozen=True)
class Move:
    dx: int
    dy: int


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Move):
        return Point(self.x + other.dx, self.y + other.dy)


Walls = set[Point]
Boxes = LBoxes = RBoxes = set[Point]
Robot = Point
Route = list[Move]


class Tile(Enum):
    WALL = "#"
    BOX = "O"
    EMPTY = "."
    ROBOT = "@"
    LBOX = "["
    RBOX = "]"


DIRECTIONS = {
    "<": Move(-1, 0),
    "^": Move(0, -1),
    ">": Move(1, 0),
    "v": Move(0, 1),
}


@dataclass
class World:
    walls: Walls
    boxes: Boxes
    robot: Robot

    @property
    def nx(self):
        if hasattr(self, "_nx"):
            return self._nx
        else:
            self._nx = max(w.x for w in self.walls)
            return self._nx

    @property
    def ny(self):
        if hasattr(self, "_ny"):
            return self._ny
        else:
            self._ny = max(w.y for w in self.walls)
            return self._ny

    def __getitem__(self, p: Point):
        if p in self.walls:
            return Tile.WALL
        elif p in self.boxes:
            return Tile.BOX
        elif p == self.robot:
            return Tile.ROBOT
        else:
            return Tile.EMPTY

    def draw(self):
        for y in range(self.ny + 1):
            for x in range(self.nx + 1):
                print(self[Point(x, y)].value, end="")
            print()

    def prepare_move(self, move: Move) -> tuple[bool, Boxes]:
        """
        Return a boolean indicating whether it is possible to move the robot
        and the set of boxes that will be moved by this move.
        """
        boxes_to_move = set()
        p = self.robot
        while True:
            p += move
            if self[p] == Tile.BOX:
                boxes_to_move.add(p)
            elif self[p] == Tile.EMPTY:
                return True, boxes_to_move
            elif self[p] == Tile.WALL:
                return False, set()

    def move_boxes(self, boxes_to_move: Boxes, move: Move) -> Boxes:
        boxes = self.boxes.difference(boxes_to_move)
        boxes = boxes.union({box + move for box in boxes_to_move})
        return boxes

    def move_robot(self, move: Move) -> Self:
        can_move, boxes_to_move = self.prepare_move(move)
        if can_move is False:
            return self
        else:
            boxes = self.move_boxes(boxes_to_move, move)
            robot = self.robot + move
            return self.__class__(self.walls, boxes, robot)


@dataclass
class World2(World):

    @classmethod
    def from_world(cls, world):
        walls, boxes = set(), set()
        for w in world.walls:
            walls.add(Point(2 * w.x, w.y))
            walls.add(Point(2 * w.x + 1, w.y))
        for b in world.boxes:
            boxes.add(Point(2 * b.x, b.y))
        robot = Point(2 * world.robot.x, world.robot.y)
        return cls(walls, boxes, robot)

    def __getitem__(self, p: Point):
        if p in self.walls:
            return Tile.WALL
        elif p in self.boxes:
            return Tile.LBOX
        elif p + Move(-1, 0) in self.boxes:
            return Tile.RBOX
        elif p == self.robot:
            return Tile.ROBOT
        else:
            return Tile.EMPTY

    def prepare_move(self, move) -> tuple[bool, Boxes]:
        boxes_to_move = set()
        q = deque()
        q.append(self.robot + move)
        while q:
            p = q.popleft()
            if self[p] == Tile.WALL:
                return False, set()
            elif self[p] == Tile.EMPTY:
                continue
            elif self[p] == Tile.LBOX:
                boxes_to_move.add(p)
                q.append(p + move)
                if move in {Move(0, 1), Move(0, -1)}:
                    q.append(p + move + Move(1, 0))
            elif self[p] == Tile.RBOX:
                boxes_to_move.add(p + Move(-1, 0))
                q.append(p + move)
                if move in {Move(0, 1), Move(0, -1)}:
                    q.append(p + move + Move(-1, 0))
        return True, boxes_to_move


def parse_data(data: str) -> tuple[World, Route]:
    walls, boxes, robot = set(), set(), None
    map, route_str = data.split("\n\n")
    route = [DIRECTIONS[c] for c in route_str.replace("\n", "")]
    for y, line in enumerate(map.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add(Point(x, y))
            elif c == "O":
                boxes.add(Point(x, y))
            elif c == "@":
                robot = Point(x, y)
    if robot is None:
        raise ValueError
    return World(walls, boxes, robot), route


data = aoc202415data.data


def part1():
    world, route = parse_data(data)
    for move in route:
        world = world.move_robot(move)
    world.draw()
    return sum(b.y * 100 + b.x for b in world.boxes)


def part2():
    world, route = parse_data(data)
    world = World2.from_world(world)
    for move in route:
        world = world.move_robot(move)
    world.draw()
    return sum(b.y * 100 + b.x for b in world.boxes)
