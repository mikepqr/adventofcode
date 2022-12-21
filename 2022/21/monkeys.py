import operator
from dataclasses import dataclass
from typing import Callable, Optional

import sympy


@dataclass
class Monkey:
    value: Optional[int | sympy.Symbol] = None
    operator: Optional[Callable[[int, int], int]] = None
    m1: Optional[str] = None
    m2: Optional[str] = None


def op_str_callable(s: str) -> Callable[[int, int], int]:
    if s == "+":
        return operator.add
    elif s == "-":
        return operator.sub
    elif s == "*":
        return operator.mul
    elif s == "/":
        return operator.truediv  # truediv required for sympy
    else:
        raise ValueError(f"Unknown operand {s}")


def parse_input(fname):
    with open(fname) as f:
        monkeys = {}
        for line in f:
            monkey, value = line.strip().split(": ")
            tokens = value.split()
            if len(tokens) == 1:
                monkeys[monkey] = Monkey(value=int(tokens[0]))
            else:
                monkeys[monkey] = Monkey(
                    operator=op_str_callable(tokens[1]), m1=tokens[0], m2=tokens[2]
                )
    return monkeys


def compute1(fname):
    monkeys = parse_input(fname)

    def compute_value(m):
        if monkeys[m].value is not None:
            return monkeys[m].value
        else:
            v1 = compute_value(monkeys[m].m1)
            v2 = compute_value(monkeys[m].m2)
            value = monkeys[m].operator(v1, v2)
            monkeys[m].value = value
            return value

    return compute_value("root")


def compute2(fname):
    monkeys = parse_input(fname)
    monkeys["humn"].value = sympy.Symbol("humn")
    for m in monkeys:
        if monkeys[m].value is None:
            monkeys[m].value = sympy.Symbol(m)

    def compute_value(m):
        if monkeys[m].m1 is None:
            return monkeys[m].value
        else:
            v1 = compute_value(monkeys[m].m1)
            v2 = compute_value(monkeys[m].m2)
            value = monkeys[m].operator(v1, v2)
            monkeys[m].value = value
            return value

    compute_value("root")

    v1 = monkeys[monkeys["root"].m1].value
    v2 = monkeys[monkeys["root"].m2].value

    humn = sympy.solve(v1 - v2, monkeys["humn"].value)

    return int(humn[0])


def test_compute1():
    assert compute1("test.txt") == 152


def test_compute2():
    assert compute2("test.txt") == 301


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
