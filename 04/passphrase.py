def load_input(fname="input.txt"):
    with open(fname) as f:
        return [line.split() for line in f.readlines()]


def part1():
    passphrases = load_input()
    valid_passphrases = [p for p in passphrases if len(p) == len(set(p))]
    return len(valid_passphrases)
