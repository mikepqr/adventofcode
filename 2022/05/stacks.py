Move = tuple[int, int, int]
Section = list[str]
Stack = list[str]


def parse_section(line: str) -> list[str]:
    n_stacks = (len(line) + 1) // 4
    return [line[4 * i + 1] for i in range(n_stacks)]


def parse_move(line: str) -> Move:
    tokens = line.split()
    return (int(tokens[1]), int(tokens[3]), int(tokens[5]))


def sections_to_stacks(sections: list[Section]) -> list[Stack]:
    stacks: list[Stack] = [[] for _ in sections[0]]
    for section in sections[::-1]:
        for i, item in enumerate(section):
            if item != " ":
                stacks[i].append(item)
    return stacks


def parse_input(fname) -> tuple[list[Section], list[Move]]:
    parse_moves = False
    sections = []
    moves = []
    with open(fname) as f:
        for line in f:
            if line == "\n":
                parse_moves = True
            elif line[1] == "1":
                pass
            elif parse_moves is False:
                sections.append(parse_section(line.strip("\n")))
            else:
                moves.append(parse_move(line.strip()))
    return sections_to_stacks(sections), moves


def compute1(fname):
    stacks, moves = parse_input(fname)
    for move in moves:
        n, source, dest = move
        for _ in range(n):
            stacks[dest - 1].append(stacks[source - 1].pop())
    return "".join(stack[-1] for stack in stacks)


def compute2(fname):
    stacks, moves = parse_input(fname)
    for move in moves:
        n, source, dest = move
        stacks[source - 1], load = stacks[source - 1][:-n], stacks[source - 1][-n:]
        stacks[dest - 1].extend(load)
    return "".join(stack[-1] for stack in stacks)


def test_compute1():
    assert compute1("test.txt") == "CMZ"


def test_compute2():
    assert compute2("test.txt") == "MCD"


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
