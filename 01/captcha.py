import itertools


def load_input(fname="input.txt"):
    with open(fname) as f:
        return [int(d) for d in f.read().strip()]


def pairwise(sequence, offset=1, circular=True):
    """
    Iterator over offset pairs of elements from sequence
    >>> list(pairwise([1, 2, 3]))
    [(1, 2), (2, 3), (3, 1)]
    >>> list(pairwise([1, 2, 3], circular=False))
    [(1, 2), (2, 3)]
    >>> list(pairwise([1, 2, 3]), offset=2)
    [(1, 3), (2, 1), (3, 2)]
    """
    a, b = itertools.tee(sequence)
    if circular:
        b = itertools.cycle(b)
    list(itertools.islice(b, offset))
    return zip(a, b)


def captcha(sequence, offset=1):
    """
    Sum of all digits that match the corresponding offset digit. Sequence is
    circular.
    >>> captcha([1, 1, 2, 2])  # 1st matches 2nd, 3rd matches 4th
    3
    >>> captcha([9, 1, 2, 1, 2, 1, 2, 9])  # last matches first
    9
    """
    return sum(l for l, r in pairwise(sequence, offset=offset) if l == r)


def part1():
    ans = captcha(load_input())
    assert ans == 1182
    return ans


def part2():
    data = load_input()
    ans = captcha(data, offset=int(len(data)/2))
    assert ans == 1152
    return ans
