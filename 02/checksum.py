import itertools


def minmax(sequence):
    "The min and max of a sequence."""
    sequence = iter(sequence)
    mn = mx = next(sequence)
    for n in sequence:
        if n < mn:
            mn = n
        if n > mx:
            mx = n
    return mn, mx


def minmaxdiff(sequence):
    "The difference between the min and max elements of a sequence."
    mn, mx = minmax(sequence)
    return mx - mn


def multiples(sequence):
    """
    Element of sequence that has a factor in sequence, and that factor.
    """
    pairs = itertools.combinations(sequence, 2)
    for a, b in pairs:
        a, b = max(a, b), min(a, b)
        if a % b == 0:
            return a, b


def multiplesdiv(sequence):
    a, b = multiples(sequence)
    return int(a/b)


def load_input(fname="input.txt"):
    with open(fname) as f:
        return [[int(n) for n in line.split()] for line in f]


def checksum(data, rowfn=minmaxdiff):
    return sum(rowfn(row) for row in data)


def part1():
    return checksum(load_input())


def part2():
    return checksum(load_input(), rowfn=multiplesdiv)
