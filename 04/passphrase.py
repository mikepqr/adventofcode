import itertools
from collections import Counter


def load_input(fname="input.txt"):
    with open(fname) as f:
        return [line.split() for line in f.readlines()]


def isanagram(s1, s2):
    """True if s1 is anagram of s2."""
    return Counter(s1) == Counter(s2)


def anyanagrams(seq):
    """
    True if any of the words in a sequence of words are anagrams of any other.
    """
    return any(isanagram(word1, word2)
               for word1, word2 in itertools.combinations(seq, 2))


def part2():
    passphrases = load_input()
    valid_passphrases = [p for p in passphrases if not anyanagrams(p)]
    ans = len(valid_passphrases)
    assert ans == 186
    return ans


def part1():
    passphrases = load_input()
    valid_passphrases = [p for p in passphrases if len(p) == len(set(p))]
    ans = len(valid_passphrases)
    assert ans == 455
    return ans
