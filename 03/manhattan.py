import itertools

import numpy as np


def coord(k, center=(0, 0)):
    """Coordinate of kth element of spiral."""
    return list(itertools.islice(spiral(center=center), k))[-1]


def manhattan(k):
    """Manhattan distance from k to 1."""
    x, y = coord(k)
    return abs(x) + abs(y)


def spiral(center=(0, 0)):
    """Iterator over coordinates of spiral."""
    mx, my = center
    x, y = center
    yield x, y
    for n in itertools.count():
        while y - my < n:
            y += 1
            yield x, y
        while x - mx > -n:
            x -= 1
            yield x, y
        while y - my > -n:
            y -= 1
            yield x, y
        while x - mx < n + 1:
            x += 1
            yield x, y


def pool(arr, x, y):
    """Sum of elements of array adjacent to arr[x, y]."""
    nx, ny = arr.shape
    elements = [arr[x + dx, y + dy]
                for dx, dy in itertools.product((-1, 0, 1), (-1, 0, 1))
                if 0 <= x + dx < nx and 0 <= y + dy < ny]
    return sum(elements)


def stress_grid(n):
    """Stress grid correct up to nth shell."""
    grid = np.zeros((2*n+1, 2*n+1), dtype=np.int)
    mx = my = n
    grid[mx, my] = 1
    for x, y in itertools.islice(spiral(center=(mx, my)), (2*n + 1)**2):
        grid[x, y] = pool(grid, x, y)
    return grid


def part1():
    ans = manhattan(368078)
    assert ans == 371
    return ans


def part2():
    sg4 = stress_grid(4)  # first value above 368078 appears in this array
    ans = min(sg4[sg4 - 368078 > 0])
    assert ans == 369601
    return ans
