def parse_input(fname) -> list[int]:
    register = [1]
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if line == "noop":
                register.append(register[-1])
            else:
                dx = int(line.split()[1])
                register.append(register[-1])
                register.append(register[-1] + dx)
    return register


def compute1(fname) -> int:
    register = parse_input(fname)
    ts = [20, 60, 100, 140, 180, 220]
    return sum(register[t - 1] * t for t in ts)


def compute2(fname) -> str:
    register = parse_input(fname)
    screen = []
    for i in range(240):
        sprite = {register[i] - 1, register[i], register[i] + 1}
        if i % 40 in sprite:
            screen.append("#")
        else:
            screen.append(".")
    newlines = [0, 40, 80, 120, 160, 200]
    return "\n".join("".join(screen[i : i + 40]) for i in newlines)


def test_compute1():
    assert compute1("test.txt") == 13140


def test_compute2():
    expected = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
    """.strip()
    print(compute2("test.txt"))
    assert compute2("test.txt") == expected


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
