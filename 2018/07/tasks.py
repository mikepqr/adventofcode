import re
from collections import defaultdict

pattern = re.compile("Step (.).*step (.)")


def load_input():
    """
    Return list of instructions, i.e. (prerequsite, task) tuples.
    """
    with open("input.txt") as f:
        return [pattern.search(line).groups() for line in f]


def make_instructions(inputs):
    """
    Returns a dict of {task: {prerequesites}}
    """
    instructions = defaultdict(set)
    for prereq, task in inputs:
        instructions[task].add(prereq)
        instructions[prereq].update({})
    return instructions


def part1():
    inputs = load_input()
    instructions = make_instructions(inputs)
    tasks = set(instructions)  # Set of all tasks
    done = set()  # Set of done tasks
    order = []  # Order of task completion

    # While tasks remain
    while tasks - done:
        # Sorted to ensure we do lexical first task if several doable
        doable = sorted(
            task
            for task, prereqs in instructions.items()
            if task not in done
            # And no prereqs left
            and not prereqs - done
        )
        done.add(doable[0])
        order.append(doable[0])
    return "".join(order)
