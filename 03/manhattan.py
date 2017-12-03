import itertools


def manhattan(k):
    """Manhattan distance from k to 1."""
    coord = list(itertools.islice(spiral(), k))[-1]
    return abs(coord[0]) + abs(coord[1])


def spiral(center=(0, 0)):
    """Iterator over coordinates of spiral."""
    x, y = center
    yield x, y
    for n in itertools.count():
        while y < n:
            y += 1
            yield x, y
        while x > -n:
            x -= 1
            yield x, y
        while y > -n:
            y -= 1
            yield x, y
        while x < n + 1:
            x += 1
            yield x, y


def part1():
    ans = manhattan(368078)
    assert ans == 371
    return ans
