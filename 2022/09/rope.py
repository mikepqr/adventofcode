from typing import Literal

Direction = Literal["R", "L", "U", "D"]
Point = tuple[int, int]


def direction_to_delta(direction: Direction) -> Point:
    if direction == "R":
        return 0, 1
    if direction == "L":
        return 0, -1
    if direction == "U":
        return 1, 0
    if direction == "D":
        return -1, 0


def move_successor(h: Point, t: Point) -> Point:
    hx, hy = h[0], h[1]
    tx, ty = t[0], t[1]
    if abs(hx - tx) > 1 or abs(hy - ty) > 1:
        if hx == tx:
            ty = ty + (1 if hy > ty else -1)
        elif hy == ty:
            tx = tx + (1 if hx > tx else -1)
        else:
            ty = ty + (1 if hy > ty else -1)
            tx = tx + (1 if hx > tx else -1)
    return tx, ty


def parse_input(fname):
    moves = []
    with open(fname) as f:
        for line in f:
            direction, distance = line.strip().split()
            distance = int(distance)
            moves.append((direction, distance))
    return moves


def compute1(fname):
    moves = parse_input(fname)
    h = 0, 0
    t = 0, 0
    visited = set()
    visited.add(t)
    for direction, distance in moves:
        dx, dy = direction_to_delta(direction)
        for _ in range(distance):
            h = h[0] + dx, h[1] + dy
            t = move_successor(h, t)
            visited.add(t)
    return len(visited)


def compute2(fname):
    moves = parse_input(fname)
    # annotation necessary to prevent this code failing pyright's checks due to
    # https://github.com/microsoft/pyright/blob/main/docs/type-inference.md#tuple-expressions
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(10)]
    visited = set()
    visited.add(rope[-1])
    for direction, distance in moves:
        dx, dy = direction_to_delta(direction)
        for _ in range(distance):
            rope[0] = rope[0][0] + dx, rope[0][1] + dy
            for i in range(1, 10):
                rope[i] = move_successor(rope[i - 1], rope[i])
            visited.add(rope[-1])
    return len(visited)


def test_compute1():
    assert compute1("test.txt") == 13


def test_compute2():
    assert compute2("test.txt") == 1
    assert compute2("test2.txt") == 36


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
