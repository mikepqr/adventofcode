import copy
import itertools
import operator
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Monkey:
    value: Optional[int] = None
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
        return operator.floordiv
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
    def compute_value(m):
        if monkeys[m].value is not None:
            return monkeys[m].value
        else:
            v1 = compute_value(monkeys[m].m1)
            v2 = compute_value(monkeys[m].m2)
            value = monkeys[m].operator(v1, v2)
            monkeys[m].value = value
            return value

    for i in itertools.count(1):
        if i % 1000 == 0:
            print(i)
        monkeys = parse_input(fname)
        monkeys["humn"].value = i
        v1 = compute_value(monkeys["root"].m1)
        v2 = compute_value(monkeys["root"].m2)
        if v1 == v2:
            return i


def test_compute1():
    assert compute1("test.txt") == 152


def test_compute2():
    assert compute2("test.txt") == 301


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
