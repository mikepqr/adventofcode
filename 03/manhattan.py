import itertools


def inside(n):
    """Tiles inside nth shell."""
    return set(range(1, (2*n+1)**2 + 1)) if n >= 0 else set()


def perimeter(n):
    """Tiles in nth shell."""
    return inside(n) - inside(n-1)


def min_shell(n):
    """Smallest tile in nth shell."""
    return min(perimeter(n))


def shell(k):
    """Shell containing k."""
    for n in itertools.count():
        if k in inside(n):
            return n


def side_length(n):
    """Length of sides of nth shell."""
    return 2*n + 1


def middles(n):
    """Tiles at the middle of the nth shell."""
    if n == 0:
        return {}
    else:
        mn = min_shell(n)
        sd = side_length(n)
        rhs_mid = mn + n - 1
        return set(rhs_mid + i*(sd-1) for i in (0, 1, 2, 3))


def manhattan(k):
    """Manhattan distance from k to 1."""
    if k == 1:
        return 0
    else:
        n = shell(k)
        mds = middles(n)
        return n + min([abs(k - md) for md in mds] +
                       [abs(md - k) for md in mds])


def part1():
    ans = manhattan(368078)
    assert ans == 371
    return ans
