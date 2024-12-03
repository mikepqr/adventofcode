import itertools
import re

with open("aoc202403.dat") as f:
    data = f.read().strip()

# data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

print(sum(int(a) * int(b) for a, b in pattern.findall(data)))

donts = re.compile(r"don't")
dos = re.compile(r"do[^n][^'][^t]")

stops = [match.span()[0] for match in donts.finditer(data)]
starts = [0] + [match.span()[0] for match in dos.finditer(data)]


def largest_smaller_than(sequence, x):
    return max([-float("inf")] + [num for num in sequence if num < x])


def is_enabled(i):
    latest_stop = largest_smaller_than(stops, i)
    latest_start = largest_smaller_than(starts, i)
    if i - latest_stop < i - latest_start:
        return False
    else:
        return True


total = 0

for match in pattern.finditer(data):
    if is_enabled(match.span()[0]):
        total += int(match.group(1)) * int(match.group(2))


# print("".join("X" if is_enabled(i) else "." for i in range(len(data))))
# print(data)
print(total)
