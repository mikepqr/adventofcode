import aoc202407data


def parse_line(line):
    result, rest = line.split(": ")
    result = int(result)
    operands = [int(s) for s in rest.split()]
    return operands, result


def solvable(operands, result, x=0, joinop=False):
    if x == result and not operands:
        return True
    if not operands:
        return False
    if x > result:
        return False

    y = operands[0]

    combinations = [x + y, (x or 1) * y]
    if joinop:
        combinations.append(int(str(x) + str(y)))

    return any(
        solvable(operands[1:], result, x=combination, joinop=joinop)
        for combination in combinations
    )


if __name__ == "__main__":
    total = 0
    for line in aoc202407data.real:
        operands, result = parse_line(line)
        if solvable(operands, result, joinop=False):
            total += result
    print(total)

    total = 0
    for line in aoc202407data.real:
        operands, result = parse_line(line)
        if solvable(operands, result, joinop=True):
            total += result
    print(total)
