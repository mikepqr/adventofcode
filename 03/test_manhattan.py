import manhattan


def test_manhattan():
    assert manhattan.manhattan(1) == 0
    assert manhattan.manhattan(12) == 3
    assert manhattan.manhattan(23) == 2
    assert manhattan.manhattan(1024) == 31
