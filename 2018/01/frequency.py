def part1():
    with open("input.txt") as f:
        result = sum(int(l) for l in f)
    assert result == 561
    return result


def part2():
    frequency = 0
    frequencies = set()
    while True:
        with open("input.txt") as f:
            for l in f:
                move = int(l)
                frequency += move
                if frequency in frequencies:
                    return frequency
                else:
                    frequencies.add(frequency)
