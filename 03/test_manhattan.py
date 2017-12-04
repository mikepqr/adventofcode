import itertools

import numpy as np

import manhattan


def test_spiral():
    ans = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1),
           (0, -1), (1, -1), (2, -1)]
    assert list(itertools.islice(manhattan.spiral(), 10)) == ans


def test_coord():
    assert manhattan.coord(23) == (0, -2)
    assert manhattan.coord(23, center=(2, 2)) == (2, 0)


def test_pool():
    arr = np.arange(9).reshape((3, 3))
    assert manhattan.pool(arr, 1, 1) == np.sum(arr)


def test_manhattan():
    assert manhattan.manhattan(1) == 0
    assert manhattan.manhattan(12) == 3
    assert manhattan.manhattan(23) == 2
    assert manhattan.manhattan(1024) == 31
