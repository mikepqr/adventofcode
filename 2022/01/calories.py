import heapq


def get_elves(fname):
    elves = [0]
    with open(fname) as f:
        for line in f:
            if line != "\n":
                elves[-1] += int(line)
            else:
                elves.append(0)
    return elves


def compute1(fname):
    elves = get_elves(fname)
    return max(elves)


def compute2(fname):
    elves = get_elves(fname)
    return sum(heapq.nlargest(3, elves))


def test_compute1():
    assert compute1("test.txt") == 24000


def test_compute2():
    assert compute2("test.txt") == 45000


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
