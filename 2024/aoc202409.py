import itertools
from typing import Generator

import aoc202409data


def unfixed_file(filemap: str) -> Generator[int | None, None, None]:
    empty = False
    block = 0
    for c in filemap:
        i = int(c)
        if not empty:
            yield from itertools.repeat(block, i)
            block += 1
        else:
            yield from itertools.repeat(None, i)
        empty = not empty


def unfixed_file_reverse(filemap: str) -> Generator[int | None, None, None]:
    empty = not len(filemap) % 2
    block = len(filemap) // 2
    for c in filemap[::-1]:
        i = int(c)
        if not empty:
            yield from itertools.repeat(block, i)
            block -= 1
        else:
            yield from itertools.repeat(None, i)
        empty = not empty


def fixed_file(filemap):
    reverse_unfixed_file = unfixed_file_reverse(filemap)
    end = len(list(unfixed_file(filemap)))
    for i, c in enumerate(unfixed_file(filemap)):
        if end <= i:
            break
        if c is not None:
            yield c
        else:
            s = next(reverse_unfixed_file)
            while s is None:
                end -= 1
                s = next(reverse_unfixed_file)
            end -= 1
            if end <= i:
                break
            yield s


def checksum(filemap):
    return sum(i * c for i, c in enumerate(fixed_file(filemap)))


test = "2333133121414131402"

data = aoc202409data.data
print(checksum(data))


def block_iter(filemap: str) -> Generator[tuple[int, int | None], None, None]:
    empty = False
    block = 0
    for c in filemap:
        i = int(c)
        if not empty:
            yield i, block
            block += 1
        else:
            yield i, None
        empty = not empty


def reverse_block_iter(filemap: str) -> Generator[tuple[int, int | None], None, None]:
    empty = not len(filemap) % 2
    block = len(filemap) // 2
    for c in filemap[::-1]:
        i = int(c)
        if not empty:
            yield i, block
            block -= 1
        else:
            yield i, None
        empty = not empty


def fixed_file2(filemap):
    yielded_blocks = set()

    for count, block in block_iter(filemap):
        if block is not None and block not in yielded_blocks:
            yield from itertools.repeat(block, count)
            yielded_blocks.add(block)
        elif block is None or block in yielded_blocks:
            reverse_blocks = reverse_block_iter(filemap)
            while count:
                for count_, block_ in reverse_blocks:
                    if (
                        block_ is not None
                        and count_ <= count
                        and block_ not in yielded_blocks
                    ):
                        yield from itertools.repeat(block_, count_)
                        yielded_blocks.add(block_)
                        count -= count_
                yield from itertools.repeat(None, count)
                break


def checksum2(filemap):
    return sum(i * int(c) for i, c in enumerate(fixed_file2(filemap)) if c)


print(checksum2(aoc202409data.data))
