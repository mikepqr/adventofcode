from dataclasses import dataclass


@dataclass
class Sensor:
    sx: int
    sy: int
    bx: int
    by: int


def parse_input(fname):
    with open(fname) as f:
        sensors = []
        for line in f:
            tokens = line.split()
            sensors.append(
                Sensor(
                    *[
                        int(token.split("=")[1].strip(",").strip(":"))
                        for token in tokens
                        if "=" in token
                    ]
                )
            )
    return sensors


def ysection(sensor, y):
    d = abs(sensor.sx - sensor.bx) + abs(sensor.sy - sensor.by)
    dx = d - abs(sensor.sy - y)
    return range(sensor.sx - dx, sensor.sx + dx + 1)


def compute1(fname, y=10):
    sensors = parse_input(fname)
    excluded = set()
    for sensor in sensors:
        excluded.update(set(ysection(sensor, y)))
        if sensor.sy == y and sensor.sx in excluded:
            excluded.remove(sensor.sx)
        if sensor.by == y and sensor.bx in excluded:
            excluded.remove(sensor.bx)

    return len(excluded)


def compute2(fname, space=20):
    sensors = parse_input(fname)
    for y in range(space + 1):
        possible = set(range(space + 1))
        excluded = set()
        for sensor in sensors:
            excluded.update(set(ysection(sensor, y)))
            if sensor.sy == y and sensor.sx in excluded:
                excluded.remove(sensor.sx)
            if sensor.by == y and sensor.bx in excluded:
                excluded.remove(sensor.bx)
        possible.difference_update(excluded)
        if possible:
            print(y, possible)

    return list(possible)[0] * 4000000 + y


def compute2_idea(fname, space):
    # for every point in the grid
    # for every sensor
    # is that point closer to the sensor than its beacon
    # if so, it cannot be where the undiscovered beacon is hiding
    # try the next point
    pass


def test_compute1():
    assert compute1("test.txt") == 26


def test_compute2():
    assert compute2("test.txt") == 56000011


if __name__ == "__main__":
    print(compute1("input.txt", y=2000000))
    print(compute2("input.txt", space=4000000))
