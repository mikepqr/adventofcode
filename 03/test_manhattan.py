import manhattan


def test_perimeter():
    assert manhattan.perimeter(0) == {1}
    assert manhattan.perimeter(1) == {2, 3, 4, 5, 6, 7, 8, 9}


def test_side_length():
    assert manhattan.side_length(0) == 1
    assert manhattan.side_length(1) == 3
    assert manhattan.side_length(2) == 5


def test_shell():
    assert manhattan.shell(1) == 0
    for i in range(2, 10):
        assert manhattan.shell(i) == 1
    for i in (10, 15, 17, 21, 23):
        assert manhattan.shell(i) == 2


def test_middles():
    assert manhattan.middles(0) == {}
    assert manhattan.middles(1) == {2, 4, 6, 8}
    assert manhattan.middles(2) == {11, 15, 19, 23}
    assert manhattan.middles(3) == {28, 34, 40, 46}


def test_manhattan():
    assert manhattan.manhattan(1) == 0
    assert manhattan.manhattan(12) == 3
    assert manhattan.manhattan(23) == 2
    assert manhattan.manhattan(1024) == 31
