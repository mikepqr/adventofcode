from collections import deque


def shortest_path(g, start, finish):
    prev = {}
    prev[start] = None
    q = deque()
    q.append(start)
    while q:
        curr = q.popleft()
        if curr == finish:
            break
        for nbr in g[curr]:
            if nbr not in prev:
                prev[nbr] = curr
                q.append(nbr)
    path = [finish]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]


def surrounding_coords(y, x, ny, nx):
    shifts = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [
        (y + dy, x + dx) for dy, dx in shifts if 0 <= y + dy < ny and 0 <= x + dx < nx
    ]


def c2h(c: str) -> int:
    if c == "S":
        return 1
    elif c == "E":
        return ord("z") - ord("a") + 1
    else:
        return ord(c) - ord("a") + 1


def parse_input(fname: str):
    g = {}
    letters = []
    with open(fname) as f:
        letters = [list(line) for line in f.readlines()]
    heights = []
    for y, row in enumerate(letters):
        height_row = []
        for x, c in enumerate(row):
            height_row.append(c2h(c))
            if c == "S":
                start = (y, x)
            elif c == "E":
                finish = (y, x)
        heights.append(height_row)
    ny = len(heights)
    nx = len(heights[0])
    for y, row in enumerate(heights):
        for x, h in enumerate(row):
            g[(y, x)] = [
                (yp, xp)
                for yp, xp in surrounding_coords(y, x, ny, nx)
                if heights[yp][xp] - h <= 1
            ]
    return g, start, finish, heights


def compute1(fname) -> int:
    g, start, finish, _ = parse_input(fname)
    return len(shortest_path(g, start, finish)) - 1


def compute2(fname) -> int:
    g, _, finish, heights = parse_input(fname)

    shortest_walk = 10000
    for y, row in enumerate(heights):
        for x, h in enumerate(row):
            if h == 1:
                try:
                    walk = len(shortest_path(g, (y, x), finish)) - 1
                    shortest_walk = min(shortest_walk, walk)
                except KeyError:
                    pass

    return shortest_walk


def test_compute1():
    assert compute1("test.txt") == 31


def test_compute2():
    assert compute2("test.txt") == 29


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
