import aoc202404data

PLUS_DIRECTIONS = {
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
}

X_DIRECTIONS = {
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
}

ALL_DIRECTIONS = PLUS_DIRECTIONS | X_DIRECTIONS

data = aoc202404data.data
NX = len(data[0])
NY = len(data)


def four_letter_words_from_here(y, x):
    for dy, dx in ALL_DIRECTIONS:
        if 0 <= x + 3 * dx < NX and 0 <= y + 3 * dy < NY:
            yield (
                data[y][x]
                + data[y + dy][x + dx]
                + data[y + 2 * dy][x + 2 * dx]
                + data[y + 3 * dy][x + 3 * dx]
            )


def three_letter_words_through_here(y, x):
    for dy, dx in X_DIRECTIONS:
        if 1 <= x < NX - 1 and 1 <= y < NY - 1:
            yield (data[y - dy][x - dx] + data[y][x] + data[y + dy][x + dx])


def n_xmas_here(x, y):
    return sum(word == "XMAS" for word in four_letter_words_from_here(y, x))


print(sum(n_xmas_here(x, y) for y, line in enumerate(data) for x, _ in enumerate(line)))


def mas_here(x, y):
    return sum(word == "MAS" for word in three_letter_words_through_here(y, x)) == 2


print(sum(mas_here(x, y) for y, line in enumerate(data) for x, _ in enumerate(line)))
