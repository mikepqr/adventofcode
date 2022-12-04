def overlap_completely(x1, x2, y1, y2):
    if x1 >= y1 and x2 <= y2:
        return True
    if y1 >= x1 and y2 <= x2:
        return True
    return False


def overlap_at_all(x1, x2, y1, y2):
    if y1 <= x1 <= y2 or y1 <= x2 <= y2:
        return True
    if x1 <= y1 <= x2 or x1 <= y2 <= x2:
        return True
    return False


def compute1(fname):
    n_overlaps = 0
    with open(fname) as f:
        for line in f:
            x12, y12 = line.strip().split(",")
            x1, x2 = map(int, x12.split("-"))
            y1, y2 = map(int, y12.split("-"))
            if overlap_completely(x1, x2, y1, y2):
                n_overlaps += 1
    return n_overlaps


def compute2(fname):
    n_overlaps = 0
    with open(fname) as f:
        for line in f:
            x12, y12 = line.strip().split(",")
            x1, x2 = map(int, x12.split("-"))
            y1, y2 = map(int, y12.split("-"))
            if overlap_at_all(x1, x2, y1, y2):
                n_overlaps += 1
    return n_overlaps


def test_compute1():
    assert compute1("test.txt") == 2


def test_compute2():
    assert compute2("test.txt") == 4


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
