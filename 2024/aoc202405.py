from collections import defaultdict
from graphlib import TopologicalSorter

import aoc202405data

rules_str, updates_str = aoc202405data.real_input.split("\n\n")
rules = [tuple(rule.split("|")) for rule in rules_str.splitlines()]
updates = [update.split(",") for update in updates_str.splitlines()]


# part 1


def valid_update(update):
    return all((update[i], update[i + 1]) in rules for i in range(len(update) - 1))


print(sum(int(update[len(update) // 2]) for update in updates if valid_update(update)))


# part 2


def construct_subgraph(pages):
    """
    Construct a graph from rules but include only edges that
    start *and* end in one of pages
    """
    g = defaultdict(set)
    for before, after in rules:
        if before in pages and after in pages:
            g[before].add(after)
    return g


def fix_update(update):
    g = construct_subgraph(update)
    return tuple(TopologicalSorter(g).static_order())


part2_total = 0
for update in updates:
    if not valid_update(update):
        fixed_update = fix_update(update)
        part2_total += int(fixed_update[len(update) // 2])

print(part2_total)
