import functools

stones = [125, 17]
stones = [9694820, 93, 54276, 1304, 314, 664481, 0, 4]


def brute_force(stones: list[int]):
    stones_ = []
    for x in stones:
        n = len(str(x))
        if x == 0:
            stones_.append(1)
        elif n % 2 == 0:
            x, y = int(str(x)[: n // 2]), int(str(x)[n // 2 :])
            stones_.extend((x, y))
        else:
            stones_.append(x * 2024)
    return stones_


for i in range(25):
    stones = brute_force(stones)

print(len(stones))


@functools.lru_cache(None)
def blink(stone: int, nblinks: int) -> int:
    if nblinks == 0:
        return 1

    n = len(str(stone))
    if stone == 0:
        stones = [1]
    elif n % 2 == 0:
        stones = [int(str(stone)[: n // 2]), int(str(stone)[n // 2 :])]
    else:
        stones = [stone * 2024]

    return sum(blink(stone, nblinks - 1) for stone in stones)


print(sum(blink(stone, 75) for stone in stones))
