import hashlib
import itertools

x = "ckczppom"
y = "abcdef"
z = "pqrstuv"


def part1(n_zeros=5):
    for i in itertools.count(1):
        s = x + str(i)
        h = hashlib.md5(s.encode()).hexdigest()
        if h[0:n_zeros] == ("0" * n_zeros):
            return i


def part2():
    return part1(n_zeros=6)


print(part1())
print(part2())
