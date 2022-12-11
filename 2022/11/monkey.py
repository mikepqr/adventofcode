import functools
import math
from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    items: list[int]
    op: Callable[[int], int]
    mod: int
    check: Callable[[int], int]
    inspected: int = 0


def check(x, mod, true_dest, false_dest):
    return true_dest if (x % mod == 0) else false_dest


def square(x):
    return x * x


def parse_input(fname: str) -> list[Monkey]:
    monkeys = []
    with open(fname) as f:
        chunks = f.read().split("\n\n")
        for chunk in chunks:
            lines = chunk.splitlines()
            items = list(map(int, lines[1].split(": ")[1].split(",")))

            operation, operand = lines[2].split()[-2:]
            if operation == "*" and operand == "old":
                op = square
            else:
                a = int(operand)
                if operation == "*":
                    op = functools.partial(lambda x, a: x * a, a=a)
                else:
                    op = functools.partial(lambda x, a: x + a, a=a)

            mod = int(lines[3].split()[-1])
            true_dest = int(lines[4].split()[-1])
            false_dest = int(lines[5].split()[-1])

            _check = functools.partial(
                check, mod=mod, true_dest=true_dest, false_dest=false_dest
            )

            monkey = Monkey(items=items, op=op, mod=mod, check=_check)
            monkeys.append(monkey)
    return monkeys


def compute1(fname) -> int:
    monkeys = parse_input(fname)
    for _ in range(20):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.items.pop()
                item = monkey.op(item)
                monkey.inspected += 1
                item = item // 3
                dest = monkey.check(item)
                monkeys[dest].items.append(item)
    inspections = sorted(monkey.inspected for monkey in monkeys)
    return inspections[-1] * inspections[-2]


def compute2(fname) -> int:
    monkeys = parse_input(fname)
    mod = math.prod(monkey.mod for monkey in monkeys)
    for _ in range(10000):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.items.pop()
                item = monkey.op(item)
                monkey.inspected += 1
                item = item % mod
                dest = monkey.check(item)
                monkeys[dest].items.append(item)
    inspections = sorted(monkey.inspected for monkey in monkeys)
    return inspections[-1] * inspections[-2]


def test_compute1():
    assert compute1("test.txt") == 10605


def test_compute2():
    assert compute2("test.txt") == 2713310158


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
