def parse_input(fname):
    valves = {}
    with open(fname) as f:
        for line in f:
            name = line.split()[1]
            rate = int(line.split("=")[1].split(";")[0])
            neighbors = [token.strip(",") for token in line.split()[9:]]
            valves[name] = {"neighbors": neighbors, "rate": rate}
    return valves


def paths(g, start, t, path=None, unopened=None):
    if path is None:
        path = []
    if unopened is None:
        unopened = {name for name in g if g[name]["rate"] > 0}

    if len(unopened) == 0:
        yield path
    elif len(path) == t + 1:
        yield path
    else:
        path = path + [start]
        for neighbor in g[start]["neighbors"]:
            yield from paths(g, neighbor, t, path=path, unopened=unopened)
            if g[start]["rate"] > 0 and len(path) < t and start in unopened:
                yield from paths(
                    g,
                    neighbor,
                    t,
                    path=path + [True],
                    unopened=unopened.difference({start}),
                )


def pressure(g, path, tmax):
    pressure = 0
    opened = set()
    for t, x in enumerate(path):
        if x is True and path[t - 1] not in opened:
            opened.add(path[t - 1])
            rate = g[path[t - 1]]["rate"]
            pressure += rate * (tmax - t)
    return pressure


def compute1(fname):
    valves = parse_input(fname)
    max_pressure = 0
    for path in paths(valves, "AA", 3):
        p = pressure(valves, path, 30)
        print(path, p)
        if p > max_pressure:
            best_path = path
            max_pressure = p
    return max_pressure


def compute2(fname):
    return -1


def test_compute1():
    assert compute1("test.txt") == 1651


def test_compute2():
    assert compute2("test.txt") == 93


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
