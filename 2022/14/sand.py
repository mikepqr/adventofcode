import functools
import itertools


def parse_input(fname):
    rocks = set()
    with open(fname) as f:
        formations = [
            [[int(x) for x in token.split(",")] for token in line.split(" -> ")]
            for line in f
        ]
    for corners in formations:
        for i in range(len(corners) - 1):
            pair = [corners[i], corners[i + 1]]
            pair.sort()
            # vertical line
            if pair[0][0] == pair[1][0]:
                rocks.update(
                    set(
                        zip(
                            itertools.repeat(pair[0][0]),
                            range(pair[0][1], pair[1][1] + 1),
                        )
                    )
                )
            # horizontal line
            else:
                rocks.update(
                    set(
                        zip(
                            range(pair[0][0], pair[1][0] + 1),
                            itertools.repeat(pair[0][1]),
                        )
                    )
                )
            # horizontal line
    return rocks


def stringify_points(points: set[tuple[int, int]], fill="#", empty=".") -> str:
    xmin = min(points, key=lambda x: x[0])[0]
    xmax = max(points, key=lambda x: x[0])[0]
    ymin = min(points, key=lambda x: x[1])[1]
    ymax = max(points, key=lambda x: x[1])[1]
    return "\n".join(
        "".join(fill if (x, y) in points else empty for x in range(xmin, xmax + 1))
        for y in range(ymin, ymax + 1)
    )


def finished_part1(blocked, maxy):
    for _, y in blocked:
        if y > maxy:
            return True
    return False


def finished_part2(blocked):
    return (500, 0) in blocked


def simulate(rocks, condition):
    maxy = max(rocks, key=lambda x: x[1])[1]
    blocked = rocks
    n_grains = 0
    while True:
        n_grains += 1
        gx, gy = 500, 0
        while True:
            if gy > maxy:
                blocked.add((gx, gy))
                break
            elif (gx, gy + 1) not in blocked:
                gx, gy = gx, gy + 1
            elif (gx - 1, gy + 1) not in blocked:
                gx, gy = gx - 1, gy + 1
            elif (gx + 1, gy + 1) not in blocked:
                gx, gy = gx + 1, gy + 1
            else:
                blocked.add((gx, gy))
                break
        if condition(blocked):
            return n_grains


def compute1(fname):
    rocks = parse_input(fname)
    maxy = max(rocks, key=lambda x: x[1])[1]
    n_grains = simulate(rocks, condition=functools.partial(finished_part1, maxy=maxy))
    return n_grains - 1


def compute2(fname):
    rocks = parse_input(fname)
    n_grains = simulate(rocks, condition=finished_part2)
    return n_grains


def test_compute1():
    assert compute1("test.txt") == 24


def test_compute2():
    assert compute2("test.txt") == 93


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
