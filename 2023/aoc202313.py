import numpy


def ascii2array(txt: str):
    lines = txt.splitlines()
    arr = numpy.zeros((len(lines), len(lines[0])), dtype=bool)
    for i, line in enumerate(lines):
        arr[i] = [c == "#" for c in line]
    return arr


def summarize_pattern(arr: numpy.ndarray, expected_difference=0) -> int:
    ny, nx = arr.shape
    for i in range(1, nx):
        width = min(i, nx - i)
        left = arr[:, i - width : i]
        # backwards slice to reflect
        right = arr[:, i + width - 1 : i - 1 : -1]
        if (left != right).sum() == expected_difference:
            return i
    for i in range(1, ny):
        height = min(i, ny - i)
        top = arr[i - height : i, :]
        bottom = arr[i + height - 1 : i - 1 : -1, :]
        if (top != bottom).sum() == expected_difference:
            return 100 * i
    # Let type checker know this will never happen
    assert False


def part1():
    return sum(summarize_pattern(ascii2array(txt)) for txt in data)


def part2():
    return sum(
        summarize_pattern(ascii2array(txt), expected_difference=1) for txt in data
    )


data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".strip().split(
    "\n\n"
)

with open("13.txt") as f:
    data = f.read().strip().split("\n\n")


if __name__ == "__main__":
    print(part1())
    print(part2())
