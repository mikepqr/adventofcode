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


def ysections(sensors, y) -> list[tuple[int, int]]:
    """
    Returns a list of the [) boundaries of the zone explored by a list of
    sensors a y=y.

    Not all sensors explore y=y, this list may be shorter than len(sensors).

                   1    1    2    2
         0    5    0    5    0    5
    -2 ..........#.................
    -1 .........###................
     0 ....S...#####...............
     1 .......#######........S.....
     2 ......#########S............
     3 .....###########SB..........
     4 ....#############...........
     5 ...###############..........
     6 ..#################.........
     7 .#########S#######S#........
     8 ..#################.........
     9 ...###############..........
    10 ....B############...........
    11 ..S..###########............
    12 ......#########.............
    13 .......#######..............
    14 ........#####.S.......S.....
    15 B........###................
    16 ..........#SB...............
    17 ................S..........B
    18 ....S.......................
    19 ............................
    20 ............S......S........
    21 ............................
    22 .......................B....

    e.g. the boundary for this sensor at y=10 is (2, 15)
    """
    boundaries = []
    for sensor in sensors:
        # Manhattan distance from sensor to its nearest beacon
        d = abs(sensor.sx - sensor.bx) + abs(sensor.sy - sensor.by)
        dx = d - abs(sensor.sy - y)
        if dx >= 0:
            left, right = sensor.sx - dx, sensor.sx + dx + 1
            boundaries.append((left, right))
    return boundaries


def compute1(fname, y=10):
    sensors = parse_input(fname)
    excluded = set()
    boundaries = ysections(sensors, y)
    for boundary in boundaries:
        excluded.update(set(range(*boundary)))
    for sensor in sensors:
        if sensor.by == y and sensor.bx in excluded:
            excluded.remove(sensor.bx)
    return len(excluded)


def compute2(fname, space=20):
    sensors = parse_input(fname)
    for y in range(space + 1):
        boundaries = ysections(sensors, y)
        # Sort boundaries by their left
        boundaries.sort()
        # Starting at the right of the 0th boundary
        x = boundaries[0][1]
        for i in range(1, len(boundaries)):
            # If the next boundary overlaps with the current location
            if boundaries[i][0] <= x:
                # Step to the right of the next boundary if it is right of the
                # current location
                x = max(x, boundaries[i][1])
            # If the next boundary does not overlap with the current location
            # then we found the gap
            else:
                return x * 4000000 + y


def test_compute1():
    assert compute1("test.txt") == 26


def test_compute2():
    assert compute2("test.txt") == 56000011


if __name__ == "__main__":
    print(compute1("input.txt", y=2000000))
    print(compute2("input.txt", space=4000000))
