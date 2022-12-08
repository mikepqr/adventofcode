def parse_input(fname):
    forest = []
    with open(fname) as f:
        for line in f:
            forest.append(list(map(int, line.strip())))
    return forest


def is_visible(row, col, forest):
    tree = forest[row][col]
    rank = forest[row]
    if not rank[:col] or max(rank[:col]) < tree:
        return True
    elif not rank[col + 1 :] or max(rank[col + 1 :]) < tree:
        return True
    file = [forest[i][col] for i in range(len(forest))]
    if not file[:row] or max(file[:row]) < tree:
        return True
    elif not file[row + 1 :] or max(file[row + 1 :]) < tree:
        return True
    return False


def viewing_distance(view, height):
    x = 0
    for tree in view:
        x += 1
        if tree >= height:
            break
    return x


def scenic_score(row, col, forest):
    view_up = [forest[i][col] for i in range(row)][::-1]
    view_left = forest[row][:col][::-1]
    view_down = [forest[i][col] for i in range(row + 1, len(forest))]
    view_right = forest[row][col + 1 :]
    height = forest[row][col]
    return (
        viewing_distance(view_up, height)
        * viewing_distance(view_left, height)
        * viewing_distance(view_down, height)
        * viewing_distance(view_right, height)
    )


def compute1(fname):
    forest = parse_input(fname)
    n_visible = sum(
        is_visible(row, col, forest)
        for row in range(len(forest))
        for col in range(len(forest[0]))
    )
    return n_visible


def compute2(fname):
    forest = parse_input(fname)
    return max(
        scenic_score(row, col, forest)
        for row in range(len(forest))
        for col in range(len(forest[0]))
    )


def test_compute1():
    assert compute1("test.txt") == 21


def test_compute2():
    assert compute2("test.txt") == 8


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
