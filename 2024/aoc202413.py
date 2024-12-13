import re

import aoc202413data
import numpy

test = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

data = aoc202413data.data
# data = test

machine_strs = data.split("\n\n")


def parse_machine_str(s):
    lines = s.splitlines()
    regex = re.compile(r"\d+")
    ax, ay = list(map(int, regex.findall(lines[0])))
    bx, by = list(map(int, regex.findall(lines[1])))
    prizex, prizey = list(map(int, regex.findall(lines[2])))
    return ax, ay, bx, by, prizex, prizey


def total_cost():
    cost = 0
    for s in machine_strs:
        ax, ay, bx, by, prizex, prizey = parse_machine_str(s)
        a = numpy.array([[ax, bx], [ay, by]])
        b = numpy.array([prizex, prizey])
        x = numpy.linalg.solve(a, b)
        if numpy.allclose(x, numpy.round(x)):
            cost += 3 * x[0] + x[1]
    return int(cost)


def total_cost2():
    cost = 0
    for s in machine_strs:
        ax, ay, bx, by, prizex, prizey = parse_machine_str(s)
        prizex += 10000000000000
        prizey += 10000000000000
        a = numpy.array([[ax, bx], [ay, by]])
        b = numpy.array([prizex, prizey])
        x = numpy.linalg.solve(a, b)
        if numpy.allclose(x, numpy.round(x), rtol=0, atol=1e-3):
            cost += 3 * x[0] + x[1]
    return int(cost)
