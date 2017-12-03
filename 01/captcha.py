import itertools

test_data = [9, 1, 2, 1, 2, 1, 2, 9]


def load_input(fname="input.txt"):
    with open(fname) as f:
        return [int(d) for d in f.read().strip()]


def pairwise(sequence, offset=1):
    """
    Generator that returns offset pairs of elements from sequence, e.g.
    >>> list(pairwise([1, 2, 3]))
    [(1, 2), (2, 3), (3, 1)]
    >>> list(pairwise([1, 2, 3]), offset=2)
    [(1, 3), (2, 1), (3, 2)]
    """
    a = iter(sequence)
    b = itertools.cycle(sequence)
    if offset:
        list(itertools.islice(b, offset))
    for l, r in zip(a, b):
        yield l, r


def captcha(sequence, offset=1):
    """
    The sum of all digits that match the corresponding offset digit. The
    sequence is circular.
    >>> captcha([1, 1, 2, 2])  # 1st matches 2nd, 3rd matches 4th
    3
    >>> captcha([9,1, 2, 1, 2, 1, 2, 9])  # last matches first
    9
    """
    return sum(l for l, r in pairwise(sequence, offset=offset) if l == r)


def part1():
    print(captcha(load_input()))


def part2():
    data = load_input()
    print(captcha(data, offset=int(len(data)/2)))
