import functools
from dataclasses import dataclass

data = """
Time:        54     81     70     88
Distance:   446   1292   1035   1007
""".strip().splitlines()

# data = """
# Time:      7  15   30
# Distance:  9  40  200
# """.strip().splitlines()


@dataclass
class Race:
    duration: int
    distance: int


def parse_input():
    durations = [int(x) for x in data[0].split(":")[1].split()]
    distances = [int(x) for x in data[1].split(":")[1].split()]
    return [
        Race(duration, distance) for duration, distance in zip(durations, distances)
    ]


def parse_input_2():
    duration = int(data[0].split(":")[1].replace(" ", ""))
    distance = int(data[1].split(":")[1].replace(" ", ""))
    return Race(duration, distance)


def distance(duration, hold):
    return hold * (duration - hold)


def n_wins(race):
    return sum(
        distance(race.duration, hold) > race.distance
        for hold in range(1, race.duration)
    )


def part1():
    races = parse_input()
    wins = [n_wins(race) for race in races]
    return functools.reduce(lambda x, y: x * y, wins, 1)


def part2():
    race = parse_input_2()
    return n_wins(race)


if __name__ == "__main__":
    print(part1())
    print(part2())
