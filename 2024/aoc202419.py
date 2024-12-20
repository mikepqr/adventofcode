import functools

import aoc202419data

pieces_str, scarves_str = aoc202419data.data.split("\n\n")
pieces = pieces_str.split(", ")
scarves = scarves_str.splitlines()


@functools.lru_cache()
def npossible(scarf: str) -> int:
    if scarf == "":
        return 1

    return sum(
        npossible(scarf[len(piece) :]) for piece in pieces if scarf.startswith(piece)
    )


def part1():
    return sum(npossible(scarf) > 0 for scarf in scarves)


def part2():
    return sum(npossible(scarf) for scarf in scarves)
