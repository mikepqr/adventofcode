import itertools
from collections import Counter


def part1():
    twos = 0
    threes = 0
    with open("input.txt") as f:
        for l in f:
            two, three = False, False
            counts = Counter(l)
            for k, v in counts.items():
                if v == 2:
                    two = True
                if v == 3:
                    three = True
            if two:
                twos += 1
            if three:
                threes += 1
    return twos * threes


def one_difference(s1, s2):
    differences = 0
    for a, b in zip(s1, s2):
        if a != b:
            differences += 1
            if differences > 1:
                return False
    if differences == 0:
        return False
    else:
        return True


def shared_chars(s1, s2):
    return "".join(a for a, b in zip(s1, s2) if a == b)


def part2():
    with open("input.txt") as f:
        words = [l.strip() for l in f]
    for s1, s2 in itertools.product(words, words):
        if one_difference(s1, s2):
            return shared_chars(s1, s2)
