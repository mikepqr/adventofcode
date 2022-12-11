import math


def op_maker(operation, operand):
    if operation == "*":
        if operand == "old":
            op = lambda x: x * x
        else:
            operand = int(operand)
            op = lambda x: x * operand
    else:
        operand = int(operand)
        op = lambda x: x + operand

    return op


def check_maker(mod, true_dest, false_dest):
    def check(x):
        return true_dest if (x % mod == 0) else false_dest

    return check


def parse_input(fname):
    monkeys = {}
    with open(fname) as f:
        while True:
            try:
                line = next(f)
                i = int(line.split()[1].strip(":"))
                monkeys[i] = {"inspected": 0}
                line = next(f)
                monkeys[i]["items"] = list(map(int, line.split(": ")[1].split(",")))
                line = next(f)
                monkeys[i]["op"] = op_maker(*line.split()[-2:])
                line = next(f)
                mod = int(line.rsplit(maxsplit=1)[-1])
                monkeys[i]["mod"] = mod
                line = next(f)
                true_dest = int(line.rsplit(maxsplit=1)[-1])
                line = next(f)
                false_dest = int(line.rsplit(maxsplit=1)[-1])
                monkeys[i]["check"] = check_maker(mod, true_dest, false_dest)
                line = next(f)
            except StopIteration:
                break
    return monkeys


def print_monkeys(monkeys):
    for monkey in monkeys.values():
        print(monkey["items"], monkey["inspected"])


def compute1(fname):
    monkeys = parse_input(fname)
    for _ in range(20):
        for monkey in monkeys.values():
            while monkey["items"]:
                item = monkey["items"].pop()
                item = monkey["op"](item)
                monkey["inspected"] += 1
                item = item // 3
                dest = monkey["check"](item)
                monkeys[dest]["items"].append(item)
    inspections = sorted(monkey["inspected"] for monkey in monkeys.values())
    return inspections[-1] * inspections[-2]


def compute2(fname) -> str:
    monkeys = parse_input(fname)
    mod = math.prod(monkey["mod"] for monkey in monkeys.values())
    for _ in range(10000):
        for monkey in monkeys.values():
            while monkey["items"]:
                item = monkey["items"].pop()
                item = monkey["op"](item)
                monkey["inspected"] += 1
                item = item % mod
                dest = monkey["check"](item)
                monkeys[dest]["items"].append(item)
    inspections = sorted(monkey["inspected"] for monkey in monkeys.values())
    return inspections[-1] * inspections[-2]


def test_compute1():
    assert compute1("test.txt") == 10605


def test_compute2():
    assert compute2("test.txt") == 2713310158


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
