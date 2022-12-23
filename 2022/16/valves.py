from collections import defaultdict, deque


def parse_input(fname):
    valves = {}
    with open(fname) as f:
        for line in f:
            name = line.split()[1]
            rate = int(line.split("=")[1].split(";")[0])
            neighbors = [token.strip(",") for token in line.split()[9:]]
            valves[name] = {"neighbors": neighbors, "rate": rate}
    return valves


def compute1(fname):
    g = parse_input(fname)

    T = 30
    # k = (current location, set opened so far)
    # v = max flow seen so far given those things
    tried = {}
    q = deque()
    # A state is a tuple of (
    #    current location,
    #    time,
    #    set of valves opened so far
    #    cumulative flow so far
    # )
    # We need the set of valves so far to determine whether a state is worth
    # pursuing, but we do not care about the order in which they were opened
    # when making this decision.
    q.append(("AA", 1, frozenset(), 0))
    best = 0

    flowers = frozenset(v for v in g if g[v]["rate"] > 0)

    while q:
        curr, t, opened, flowed = q.popleft()
        print(len(opened))

        if t > T:
            best = max(best, flowed)
            continue

        if opened == flowers:
            # if everything is open then fast forward the cumulative flow
            # computation
            flowed += (T - t + 1) * sum(g[v]["rate"] for v in opened)
            best = max(best, flowed)
            continue

        # if cumulative flow is not the best cumulative flow seen so far in the
        # same position, with the same valves open then there is no point
        # continuing with this path
        if (curr, opened) in tried and flowed <= tried[(curr, opened)]:
            continue
        else:
            tried[(curr, opened)] = flowed
            # accumulate flow
            flowed += sum(g[v]["rate"] for v in opened)
            # if curr is unopened and has flow
            if curr in flowers and curr not in opened:
                # add the state where curr is opened at this time to the queue
                q.append((curr, t + 1, opened.union({curr}), flowed))
            # add the states where we don't open curr but instead go to its
            # neighbors to the queue
            for nbr in g[curr]["neighbors"]:
                q.append((nbr, t + 1, opened, flowed))

    return best


def compute2(fname):
    g = parse_input(fname)
    flowers = frozenset(v for v in g if g[v]["rate"] > 0)

    T = 26
    # k = (current human location, current elephant location, set opened so far)
    # v = max flow seen so far given those things
    tried = {}
    q = deque()
    # A state is a tuple of (
    #    current human location,
    #    current elephant location,
    #    time,
    #    set of valves opened so far
    #    cumulative flow so far
    # )
    q.append(("AA", "AA", 1, frozenset(), 0))
    best = 0
    maxt = 0

    while q:
        me, elephant, t, opened, flowed = q.popleft()
        if t > maxt:
            print(t)
            maxt = t

        if t > T:
            if flowed > best:
                print(flowed)
                best = flowed
            continue

        if opened == flowers:
            flowed += (T - t + 1) * sum(g[v]["rate"] for v in opened)
            if flowed > best:
                print(flowed)
                best = flowed
            continue

        if (me, elephant, opened) in tried and flowed <= tried[(me, elephant, opened)]:
            continue
        if (elephant, me, opened) in tried and flowed <= tried[(elephant, me, opened)]:
            continue
        else:
            tried[(me, elephant, opened)] = flowed
            flowed += sum(g[v]["rate"] for v in opened)
            # I open, elephant moves
            if me in flowers and me not in opened:
                for nbr in g[elephant]["neighbors"]:
                    q.append((me, nbr, t + 1, opened.union({me}), flowed))
            # I move, elephant opens
            if elephant in flowers and elephant not in opened:
                for nbr in g[me]["neighbors"]:
                    q.append((nbr, elephant, t + 1, opened.union({elephant}), flowed))
            # Both move
            for e_nbr in g[elephant]["neighbors"]:
                for h_nbr in g[me]["neighbors"]:
                    q.append((h_nbr, e_nbr, t + 1, opened, flowed))

    return best


def test_compute1():
    assert compute1("test.txt") == 1651


def test_compute1_input():
    assert compute1("input.txt") == 1720


def test_compute2():
    assert compute2("test.txt") == 93


if __name__ == "__main__":
    # print(compute1("input.txt"))
    print(compute2("input.txt"))
