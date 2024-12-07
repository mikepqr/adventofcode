from dataclasses import dataclass

import aoc202606data
import tqdm

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

NEXT_DIRECTION = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}


@dataclass(frozen=True)
class Guard:
    x: int
    y: int
    dx: int
    dy: int


def move(guard, obstacles):
    x_, y_ = guard.x + guard.dx, guard.y + guard.dy
    # raise if we're about to move off the map
    if any((x_ < 0, y_ < 0, x_ >= NX, y_ >= NY)):
        raise IndexError
    # turn right if we're about to hit an obstacle
    elif (x_, y_) in obstacles:
        dx_, dy_ = NEXT_DIRECTION[(guard.dx, guard.dy)]
        return Guard(guard.x, guard.y, dx_, dy_)
    else:
        return Guard(x_, y_, guard.dx, guard.dy)


def print_map(map, visited=None):
    if visited is None:
        visited = set()
    for y, line in enumerate(map):
        print("".join("X" if (x, y) in visited else c for x, c in enumerate(line)))


def find_guard(map):
    for y, line in enumerate(map):
        for x, c in enumerate(line):
            if c == "^":
                return Guard(x, y, *UP)
            elif c == ">":
                return Guard(x, y, *RIGHT)
            elif c == "v":
                return Guard(x, y, *DOWN)
            elif c == "<":
                return Guard(x, y, *LEFT)
    raise


def find_obstacles(map):
    return {
        (x, y) for y, line in enumerate(map) for x, c in enumerate(line) if c == "#"
    }


def explore(map):
    guard = find_guard(map)
    obstacles = find_obstacles(map)
    visited = set()
    visited.add((guard.x, guard.y))
    while True:
        try:
            guard = move(guard, obstacles)
        except IndexError:
            break
        visited.add((guard.x, guard.y))
    return visited


def in_loop(guard, obstacles):
    guards = set()
    guards.add(guard)

    while True:
        try:
            guard = move(guard, obstacles)
        except IndexError:
            return False
        if guard in guards:
            return True
        guards.add(guard)


def find_loops(map, possible_obstacles):
    guard = find_guard(map)
    obstacles = find_obstacles(map)

    return sum(
        in_loop(guard, obstacles | {(x, y)}) for x, y in tqdm.tqdm(possible_obstacles)
    )


if __name__ == "__main__":
    # map = aoc202606data.test
    map = aoc202606data.real

    map = [list(line) for line in map]
    NX = len(map[0])
    NY = len(map)

    visited = explore(map)
    print(len(visited))
    n_loops = find_loops(map, possible_obstacles=visited)
    print(n_loops)
