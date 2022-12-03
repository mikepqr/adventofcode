def priority(c: str) -> int:
    if c.islower():
        return ord(c) - 96
    else:
        return ord(c) - 38


def compute1(fname):
    score = 0
    with open(fname) as f:
        for line in f:
            line = line.strip()
            n = len(line)
            compartment1, compartment2 = set(line[: n // 2]), set(line[n // 2 :])
            duplicate = list(compartment1.intersection(compartment2))[0]
            score += priority(duplicate)
    return score


def compute2(fname):
    score = 0
    with open(fname) as f:
        while True:
            try:
                r1, r2, r3 = (
                    set(next(f).strip()),
                    set(next(f).strip()),
                    set(next(f).strip()),
                )
            except StopIteration:
                break
            duplicate = list(r1.intersection(r2).intersection(r3))[0]
            score += priority(duplicate)
    return score


def test_compute1():
    assert compute1("test.txt") == 157


def test_compute2():
    assert compute2("test.txt") == 70


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
