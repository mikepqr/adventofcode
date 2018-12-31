from collections import defaultdict

import tqdm


def find_reactions(chain):
    """
    Return set containing indices items in chain that react.
    """
    reactions = set()
    i = 0
    while i < len(chain) - 1:
        a = chain[i]
        b = chain[i+1]
        # Same letter, different case
        if a.upper() == b.upper() and a != b:
            reactions.update({i, i+1})
            i += 1
        i += 1
    return reactions


def react(chain):
    """
    Delete reactive items from chain until no longer possible.
    """
    if len(chain) > 1:
        reactions = find_reactions(chain)
        if reactions:
            # Delete reactive items
            chain = "".join(c for i, c in enumerate(chain) if i not in reactions)
            # Recurse
            chain = react(chain)
    # Base case when len(chain) < 2 or no reactions
    return chain


def part1():
    with open("input.txt") as f:
        chain = f.readline().strip()
    solution = len(react(chain))
    assert solution == 10450
    return solution


def part2():
    with open("input.txt") as f:
        chain = f.readline().strip()
    lengths = defaultdict(int)
    for unit in tqdm.tqdm(set(chain.upper())):
        chain_without_unit = "".join(c for c in chain if c.upper() != unit)
        lengths[unit] = len(react(chain_without_unit))
    return min(lengths.items(), key=lambda x: x[1])
