import itertools
import re
from collections import Counter
from dataclasses import dataclass

test = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""".splitlines()

test2 = "p=2,4 v=2,-3".splitlines()

data = """\
p=80,75 v=69,72
p=88,10 v=-28,-23
p=79,61 v=79,59
p=37,102 v=92,-43
p=12,22 v=-5,-95
p=60,13 v=-30,-42
p=3,59 v=-96,-88
p=85,33 v=-43,-41
p=44,14 v=63,45
p=6,6 v=-34,-86
p=47,102 v=12,42
p=36,88 v=-88,-93
p=78,27 v=-18,52
p=96,64 v=-62,-34
p=49,99 v=-78,-15
p=57,31 v=-80,21
p=25,57 v=8,-84
p=69,20 v=81,61
p=80,5 v=-11,-30
p=2,35 v=-85,77
p=9,12 v=-4,36
p=37,68 v=12,-69
p=47,88 v=-8,-90
p=72,68 v=59,-86
p=55,38 v=-68,-94
p=60,58 v=41,37
p=76,87 v=-1,-18
p=89,9 v=38,92
p=100,67 v=17,-53
p=83,73 v=80,32
p=77,19 v=-54,-20
p=10,86 v=-65,36
p=13,88 v=-64,-84
p=50,29 v=-17,-29
p=79,38 v=89,-57
p=55,57 v=-68,22
p=71,82 v=-80,52
p=37,83 v=-68,-43
p=25,5 v=81,-22
p=83,54 v=-32,-75
p=27,95 v=-77,-55
p=70,97 v=-72,-4
p=3,84 v=-60,-60
p=16,29 v=-35,99
p=39,39 v=37,-38
p=76,94 v=90,60
p=18,21 v=-86,-26
p=22,84 v=-16,66
p=45,83 v=-40,-43
p=35,52 v=54,3
p=30,21 v=14,36
p=69,61 v=69,-66
p=52,22 v=-28,33
p=9,21 v=-85,-73
p=87,32 v=79,52
p=28,85 v=-35,85
p=32,58 v=-49,89
p=22,75 v=85,44
p=45,19 v=-88,61
p=97,59 v=98,-75
p=70,81 v=82,7
p=97,102 v=-23,-8
p=92,68 v=89,72
p=24,42 v=-63,-97
p=21,64 v=-45,-47
p=58,3 v=-69,51
p=33,68 v=19,-20
p=27,6 v=-89,-21
p=28,81 v=-67,-8
p=59,83 v=-66,-82
p=3,14 v=-3,-1
p=19,65 v=15,-25
p=57,37 v=53,-29
p=36,84 v=-4,-84
p=55,96 v=82,-21
p=68,101 v=51,51
p=68,8 v=-90,-30
p=78,51 v=-51,-63
p=4,55 v=-63,97
p=100,60 v=76,-13
p=7,91 v=-96,-73
p=97,17 v=-54,33
p=85,60 v=69,-3
p=20,39 v=96,-85
p=24,12 v=86,-84
p=34,7 v=-7,-36
p=30,69 v=-67,97
p=65,17 v=20,33
p=39,101 v=-7,-83
p=38,51 v=-90,-4
p=99,61 v=-13,59
p=30,1 v=-67,-96
p=1,89 v=-85,-83
p=8,1 v=68,4
p=89,89 v=-52,85
p=81,5 v=-55,71
p=99,60 v=-94,-72
p=68,70 v=-10,78
p=81,18 v=89,-95
p=47,61 v=-39,56
p=91,71 v=85,59
p=28,66 v=44,-28
p=10,64 v=-59,-4
p=84,10 v=-32,-11
p=29,52 v=-37,34
p=78,43 v=-92,12
p=85,3 v=-71,4
p=37,85 v=-46,-84
p=56,21 v=21,-32
p=17,17 v=15,17
p=26,87 v=45,-93
p=57,21 v=-6,40
p=95,48 v=-33,59
p=38,59 v=65,-72
p=59,85 v=-50,-99
p=17,21 v=86,-45
p=53,3 v=-28,-46
p=1,40 v=-54,-91
p=61,13 v=-40,83
p=33,35 v=-72,-96
p=40,14 v=33,-8
p=29,89 v=53,-59
p=74,0 v=-22,-42
p=12,32 v=-65,-4
p=82,89 v=-12,20
p=35,71 v=-40,20
p=14,5 v=95,83
p=46,44 v=39,92
p=25,54 v=-66,-47
p=91,78 v=64,53
p=14,9 v=25,67
p=39,29 v=-29,8
p=20,100 v=95,51
p=59,41 v=92,-82
p=15,92 v=93,-73
p=42,93 v=3,-86
p=82,93 v=-21,-96
p=50,9 v=12,-39
p=81,22 v=-13,99
p=72,81 v=-51,-93
p=88,19 v=-72,-14
p=8,93 v=-85,-15
p=54,2 v=61,8
p=44,81 v=66,41
p=78,10 v=90,8
p=19,53 v=68,4
p=80,43 v=9,46
p=11,38 v=-66,88
p=31,3 v=4,-2
p=49,28 v=-74,21
p=27,15 v=54,-88
p=96,87 v=-50,-67
p=94,94 v=-5,-97
p=16,89 v=73,23
p=93,32 v=-53,93
p=47,17 v=-29,92
p=10,78 v=16,35
p=55,33 v=-60,-17
p=55,73 v=-68,-22
p=100,62 v=17,-69
p=67,91 v=-49,45
p=68,53 v=-42,-41
p=35,73 v=54,47
p=20,63 v=-85,-12
p=23,16 v=-87,33
p=70,55 v=50,-16
p=92,6 v=41,-59
p=9,97 v=-37,47
p=48,48 v=42,40
p=96,37 v=-90,32
p=66,13 v=-60,91
p=62,46 v=-50,18
p=11,15 v=98,77
p=42,78 v=1,47
p=10,40 v=15,-48
p=88,44 v=7,-75
p=27,53 v=-70,-9
p=21,7 v=-56,96
p=92,81 v=-22,69
p=57,65 v=92,-34
p=85,63 v=77,11
p=92,2 v=-30,21
p=59,16 v=73,-70
p=16,11 v=86,-89
p=82,16 v=80,-36
p=41,30 v=-49,19
p=13,6 v=14,73
p=67,99 v=-91,51
p=37,20 v=-65,-37
p=85,16 v=99,-14
p=1,39 v=-44,56
p=37,29 v=74,5
p=44,51 v=-18,93
p=43,9 v=-55,-84
p=5,10 v=-65,26
p=51,90 v=-59,-96
p=55,98 v=-9,23
p=0,94 v=88,-49
p=91,43 v=-14,-72
p=93,43 v=-69,-94
p=84,100 v=-12,54
p=23,46 v=85,78
p=79,37 v=39,-10
p=1,23 v=99,-79
p=73,50 v=-51,84
p=78,58 v=-31,-16
p=75,44 v=69,71
p=27,5 v=-87,14
p=95,91 v=-33,63
p=22,94 v=-5,-37
p=36,11 v=-5,-60
p=18,3 v=-64,-27
p=44,14 v=24,-92
p=96,40 v=65,-92
p=47,1 v=84,25
p=93,22 v=68,-48
p=14,32 v=-24,37
p=99,17 v=78,-89
p=53,36 v=10,58
p=44,44 v=-78,-60
p=15,28 v=-96,-20
p=96,61 v=-81,-45
p=58,87 v=-9,7
p=20,43 v=84,-22
p=50,42 v=-18,68
p=74,23 v=-12,42
p=12,57 v=-94,-94
p=49,49 v=-89,40
p=47,98 v=-67,-8
p=84,17 v=-62,11
p=31,6 v=-57,-42
p=28,67 v=66,-81
p=0,3 v=-88,-13
p=51,76 v=82,76
p=67,81 v=87,-14
p=84,78 v=39,41
p=39,74 v=72,35
p=30,10 v=64,-77
p=10,31 v=11,-4
p=6,90 v=-4,76
p=90,24 v=-2,-23
p=8,39 v=-57,-27
p=31,69 v=93,-25
p=79,38 v=39,-35
p=69,31 v=70,30
p=1,16 v=7,73
p=46,9 v=-99,-70
p=53,16 v=-94,-84
p=32,60 v=33,-69
p=62,22 v=-99,-4
p=66,3 v=98,20
p=4,76 v=46,-75
p=50,71 v=-90,22
p=57,12 v=31,-15
p=59,84 v=-50,-65
p=33,0 v=76,-48
p=58,76 v=-30,44
p=6,69 v=6,35
p=74,91 v=-61,-43
p=36,92 v=-58,60
p=2,78 v=-48,-98
p=43,91 v=53,76
p=34,101 v=-77,79
p=40,44 v=-68,28
p=71,64 v=47,-48
p=54,7 v=84,15
p=54,75 v=-60,-31
p=14,40 v=86,12
p=80,29 v=-92,-26
p=8,47 v=-33,-69
p=2,41 v=12,-9
p=39,60 v=-38,59
p=13,22 v=86,-20
p=25,12 v=-57,11
p=60,47 v=96,96
p=50,51 v=-48,-82
p=85,40 v=89,74
p=99,4 v=-94,-21
p=75,7 v=29,-73
p=28,58 v=-80,24
p=46,94 v=-9,56
p=24,65 v=-76,62
p=50,2 v=-20,70
p=85,55 v=-5,66
p=38,11 v=43,36
p=53,54 v=53,24
p=18,45 v=65,96
p=94,22 v=16,80
p=79,28 v=75,-69
p=30,38 v=-15,-29
p=5,23 v=-4,49
p=8,98 v=96,-99
p=7,60 v=-14,47
p=96,17 v=88,-73
p=48,23 v=-41,35
p=17,31 v=-26,-23
p=13,52 v=66,37
p=58,19 v=41,55
p=25,9 v=-77,-89
p=3,92 v=55,-80
p=74,95 v=20,-77
p=26,70 v=43,72
p=54,4 v=96,-18
p=63,8 v=-97,49
p=23,51 v=87,-75
p=24,18 v=85,36
p=8,52 v=6,-13
p=97,50 v=17,-72
p=47,66 v=-25,6
p=38,78 v=3,-93
p=62,6 v=5,77
p=56,74 v=-70,-6
p=94,99 v=9,34
p=19,92 v=-18,26
p=35,54 v=-47,-69
p=92,8 v=-13,42
p=47,86 v=12,-90
p=12,83 v=-68,2
p=0,18 v=-75,-89
p=11,99 v=-99,14
p=88,20 v=62,21
p=27,53 v=53,-47
p=17,44 v=-5,-91
p=57,10 v=66,-65
p=66,95 v=-71,-12
p=38,21 v=23,95
p=68,69 v=-31,35
p=87,71 v=50,72
p=98,12 v=47,33
p=94,21 v=66,51
p=53,97 v=-16,-93
p=59,35 v=6,39
p=12,88 v=-86,88
p=85,16 v=39,8
p=38,85 v=35,80
p=44,9 v=-48,11
p=71,18 v=-82,39
p=85,14 v=-74,-73
p=88,22 v=-42,36
p=8,6 v=-58,38
p=21,58 v=-66,9
p=25,17 v=-68,95
p=89,16 v=-34,-86
p=33,54 v=64,-88
p=57,8 v=54,51
p=40,18 v=-98,58
p=91,22 v=-34,-53
p=75,81 v=-70,26
p=89,70 v=-2,69
p=62,6 v=-1,-92
p=78,24 v=-82,-42
p=47,7 v=-75,83
p=86,8 v=-63,95
p=80,64 v=-36,-79
p=69,95 v=-30,29
p=46,86 v=85,20
p=76,35 v=-82,-51
p=33,15 v=-17,55
p=40,58 v=-2,-11
p=76,31 v=39,2
p=46,82 v=-15,-45
p=14,53 v=36,-16
p=98,66 v=68,-3
p=83,38 v=35,-87
p=41,9 v=53,70
p=35,33 v=-68,-68
p=53,66 v=62,97
p=75,80 v=49,-62
p=66,70 v=-50,47
p=78,80 v=7,64
p=82,16 v=85,-81
p=58,25 v=11,-70
p=36,72 v=33,72
p=66,92 v=-91,10
p=24,52 v=-98,22
p=74,7 v=-36,-79
p=46,26 v=-61,-90
p=52,24 v=53,-88
p=92,26 v=31,78
p=60,52 v=80,-81
p=82,78 v=-81,-49
p=10,3 v=-15,-55
p=91,31 v=99,77
p=75,50 v=-91,40
p=49,71 v=93,91
p=1,94 v=-54,54
p=96,50 v=39,18
p=0,3 v=-53,33
p=34,9 v=-17,-8
p=96,28 v=68,-63
p=25,4 v=66,21
p=94,74 v=82,-89
p=47,66 v=-17,87
p=58,23 v=63,83
p=13,82 v=-74,75
p=29,85 v=40,79
p=57,7 v=50,83
p=7,88 v=-37,-16
p=81,61 v=-10,34
p=6,32 v=33,-60
p=63,7 v=1,98
p=59,29 v=-31,-85
p=85,91 v=19,-18
p=22,39 v=21,90
p=25,13 v=75,89
p=14,100 v=-27,30
p=33,6 v=97,-53
p=84,83 v=-22,38
p=100,69 v=77,-38
p=2,67 v=-14,-25
p=71,71 v=-53,73
p=9,43 v=-52,98
p=55,76 v=-60,94
p=49,91 v=-35,-95
p=77,68 v=26,12
p=41,91 v=-17,-15
p=1,69 v=-44,72
p=32,61 v=4,59
p=94,12 v=-33,30
p=1,35 v=96,49
p=72,64 v=-61,-53
p=76,93 v=38,-37
p=97,9 v=33,61
p=60,32 v=80,18
p=16,68 v=15,-29
p=99,72 v=66,44
p=99,18 v=56,99
p=42,11 v=-88,11
p=57,69 v=-2,-2
p=39,57 v=26,-51
p=34,15 v=73,42
p=56,55 v=-61,-75
p=89,1 v=67,-27
p=21,100 v=5,70
p=85,11 v=-35,63
p=16,35 v=47,-63
p=98,0 v=93,-2
p=51,89 v=-9,85
p=50,32 v=84,-42
p=29,63 v=78,-76
p=92,86 v=89,10
p=27,11 v=-77,51
p=65,21 v=-59,68
p=84,68 v=20,-50
p=19,2 v=-24,-36
p=25,78 v=25,-85
p=90,92 v=59,-87
p=70,100 v=10,-52
p=48,78 v=3,54
p=85,81 v=30,44
p=53,65 v=41,-67
p=13,95 v=82,-29
p=5,19 v=95,75
p=37,96 v=-68,26
p=83,16 v=-5,-9
p=31,17 v=4,-20
p=83,34 v=-83,-76
p=50,88 v=93,-5
p=66,36 v=-30,58
p=11,29 v=-44,83
p=31,31 v=-77,-51
p=26,85 v=14,-18
p=8,76 v=65,69
p=60,70 v=-40,47
p=69,70 v=22,64
p=85,53 v=18,12
p=97,93 v=-58,-57
p=52,83 v=92,-9
p=20,92 v=30,50
p=88,73 v=32,3
p=83,16 v=-42,-14
p=57,89 v=-29,20
p=50,19 v=73,8
p=8,101 v=-94,-68
p=12,77 v=-4,-84
p=63,28 v=-84,91
p=46,25 v=13,-95
p=93,21 v=88,-26
p=10,54 v=-24,72
p=69,16 v=-92,-30
p=26,68 v=21,97
p=56,30 v=-90,-51
p=62,69 v=-1,-50
p=7,6 v=55,-39
p=63,78 v=76,92
p=57,55 v=-51,-19
p=70,62 v=18,37
p=88,26 v=-61,82
p=80,50 v=-73,99
p=40,1 v=-78,86
p=35,85 v=81,-12
p=17,74 v=56,47
p=36,99 v=64,-15
p=56,18 v=-29,-14
p=42,44 v=-18,46
p=84,4 v=-63,-2
p=97,75 v=27,-62
p=47,71 v=54,-50
p=26,101 v=-67,-83
p=30,74 v=-57,66""".splitlines()


NX = 101
NY = 103

regex = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int


def parse_line(line) -> Robot:
    match = regex.match(line)
    if match:
        return Robot(*map(int, match.groups()))
    raise ValueError(f"{line} does not match {regex}")


def draw(robots: list[Robot]) -> None:
    counts = Counter((robot.x, robot.y) for robot in robots)
    lines = []
    for y in range(NY):
        lines.append(
            "".join(str(counts[(x, y)]) if counts[(x, y)] else "." for x in range(NX))
        )
    print("\n".join(lines))


def advance_robot(robot: Robot, seconds: int):
    x_ = (robot.x + robot.dx * seconds) % NX
    y_ = (robot.y + robot.dy * seconds) % NY
    return Robot(x_, y_, robot.dx, robot.dy)


def basic_test():
    robot = parse_line(test2[0])
    draw([robot])
    for _ in range(5):
        input()
        robot = advance_robot(robot, 1)
        draw([robot])


def safety_factor(robots):
    quadrants = Counter()
    for robot in robots:
        if 0 <= robot.x < NX // 2 and 0 <= robot.y < NY // 2:
            quadrants[0] += 1
        if NX // 2 < robot.x < NX and 0 <= robot.y < NY // 2:
            quadrants[1] += 1
        if 0 <= robot.x < NX // 2 and NY // 2 < robot.y < NY:
            quadrants[2] += 1
        if NX // 2 < robot.x < NX and NY // 2 < robot.y < NY:
            quadrants[3] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def part1():
    robots = [parse_line(line) for line in data]
    robots = [advance_robot(robot, 100) for robot in robots]
    print(safety_factor(robots))


def part2():
    robots = [parse_line(line) for line in data]
    min_safety_factor = float("inf")
    safest_time = 0
    for t in range(10000):
        if safety_factor(robots) < min_safety_factor:
            min_safety_factor = safety_factor(robots)
            print(t, min_safety_factor)
            safest_time = t
            draw(robots)
        robots = [advance_robot(robot, 1) for robot in robots]
    return safest_time
