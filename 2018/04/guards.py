import re
from collections import defaultdict
from operator import itemgetter

linepat = re.compile("\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.*)")
guardpat = re.compile("#(\d+)")


def parse_line(line):
    event = {}
    (event["year"],
     event["month"],
     event["date"],
     event["hour"],
     event["minute"],
     event["description"]) = linepat.search(line).groups()
    event["minute"] = int(event["minute"])
    return event


with open("input.txt") as f:
    lines = sorted(line.strip() for line in f.readlines())

# {guard: count} total minutes each guard slept
total_slept = defaultdict(int)

# {guard: {minute: count}} number of times each guard was asleep that minute
times_slept = defaultdict(lambda: defaultdict(int))

for event in [parse_line(line) for line in lines]:
    if "#" in event["description"]:
        guard = int(guardpat.search(event["description"]).group(1))
    if "asleep" in event["description"]:
        asleep_minute = event["minute"]
    if "wakes" in event["description"]:
        wake_minute = event["minute"]
        for minute in range(asleep_minute, wake_minute):
            total_slept[guard] += 1
            times_slept[guard][minute] += 1


value = itemgetter(1)


def part1():
    chosen_guard = max(total_slept.items(), key=value)[0]
    chosen_time = max(times_slept[chosen_guard].items(), key=value)[0]
    assert chosen_guard == 521
    assert chosen_time == 24
    return chosen_guard * chosen_time


def part2():
    max_times_by_guard = [(guard, max(times.items(), key=value))
                          for guard, times in times_slept.items()]
    chosen_guard, (chosen_time, _) = max(max_times_by_guard, key=lambda x: x[1][1])
    assert chosen_guard == 2969
    assert chosen_time == 47
    return chosen_guard * chosen_time
