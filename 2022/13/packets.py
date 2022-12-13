import functools
import json


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    elif isinstance(left, int):
        return compare([left], right)
    elif isinstance(right, int):
        return compare(left, [right])
    else:
        if not left and not right:
            return 0
        elif left == []:
            return -1
        elif right == []:
            return 1
        else:
            lhead, *ltail = left
            rhead, *rtail = right
            return compare(lhead, rhead) or compare(ltail, rtail)


def parse_input(fname):
    with open(fname) as f:
        chunks = f.read().split("\n\n")
    return [[json.loads(line) for line in chunk.splitlines()] for chunk in chunks]


def compute1(fname):
    pairs = parse_input(fname)
    return sum(
        i for i, (left, right) in enumerate(pairs, 1) if compare(left, right) < 0
    )


def compute2(fname):
    pairs = parse_input(fname)
    signals = sum([pair for pair in pairs], [])
    signals.append([[2]])
    signals.append([[6]])
    signals.sort(key=functools.cmp_to_key(compare))
    for i, signal in enumerate(signals, 1):
        if signal == [[2]]:
            x = i
        if signal == [[6]]:
            return x * i


def test_compute1():
    assert compute1("test.txt") == 13


def test_compute2():
    assert compute2("test.txt") == 140


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
