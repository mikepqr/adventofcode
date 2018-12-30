from collections import defaultdict


def parse_line(ln):
    words = ln.split()
    claim_id = words[0].split("#")[1]
    x = words[2].split(",")[0]
    y = words[2].split(",")[1].strip(":")
    width, length = words[3].split("x")
    claim = {
        "claim_id": claim_id,
        "x": int(x),
        "y": int(y),
        "width": int(width),
        "length": int(length),
    }
    claim["squares"] = occupy(claim)
    return claim


def occupy(claim):
    """
    Return coordinates of patches occupied by claim.
    """
    coordinates = []
    for dx in range(claim["width"]):
        for dy in range(claim["length"]):
            coordinates.append((claim["x"] + dx, claim["y"] + dy))
    return coordinates


def allocate_cloth():
    """
    Build dict that maps (x,y) locations to set of claim ids claiming that location
    """
    cloth = defaultdict(set)
    with open("input.txt") as f:
        claims = (parse_line(ln) for ln in f)
        for claim in claims:
            for square in claim["squares"]:
                cloth[square].add(claim["claim_id"])
    return cloth


def part1():
    cloth = allocate_cloth()
    double_claimed = [square for square, ids in cloth.items() if len(ids) > 1]
    n_double_claimed = len(double_claimed)
    assert n_double_claimed == 113966
    return n_double_claimed


def part2():
    cloth = allocate_cloth()
    all_ids = set()
    invalid_ids = set()
    for ids in cloth.values():
        all_ids.update(ids)
        if len(ids) > 1:
            invalid_ids.update(ids)
    solution = all_ids.difference(invalid_ids)
    assert len(solution) == 1
    return solution.pop()
