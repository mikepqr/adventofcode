def compute(fname, n=4):
    with open(fname) as f:
        data = f.read().strip()
    for i in range(len(data) - n - 1):
        if len(set(data[i : i + n])) == n:
            return i + n


def test_compute1():
    assert compute("test1.txt", n=4) == 7
    assert compute("test2.txt", n=4) == 5
    assert compute("test3.txt", n=4) == 6
    assert compute("test4.txt", n=4) == 10
    assert compute("test5.txt", n=4) == 11


def test_compute2():
    assert compute("test1.txt", n=14) == 19
    assert compute("test2.txt", n=14) == 23
    assert compute("test3.txt", n=14) == 23
    assert compute("test4.txt", n=14) == 29
    assert compute("test5.txt", n=14) == 26


if __name__ == "__main__":
    print(compute("input.txt", n=4))
    print(compute("input.txt", n=14))
