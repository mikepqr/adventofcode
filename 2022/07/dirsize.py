import os


def parse_listing(fname):
    dirs = {}
    name = "/"
    with open(fname) as f:
        try:
            while True:
                line = next(f).strip()
                if line.startswith("$ cd .."):
                    name = os.path.split(name)[0]
                elif line.startswith("$ cd"):
                    if line.split()[-1] == "/":
                        name = "/"
                    else:
                        name = os.path.join(name, line.split()[-1])
                    dirs[name] = {"file_size": 0, "subdirs": []}
                    _ = next(f)  # discard `$ ls`
                    continue
                elif line.startswith("dir"):
                    dirs[name]["subdirs"].append(os.path.join(name, line.split()[-1]))
                else:
                    dirs[name]["file_size"] += int(line.split()[0])
        except StopIteration:
            pass
    return dirs


def size(d, dirs):
    if "total_size" in dirs[d]:
        return dirs[d]["total_size"]
    elif not dirs[d]["subdirs"]:
        dirs[d]["total_size"] = dirs[d]["file_size"]
    else:
        dirs[d]["total_size"] = dirs[d]["file_size"] + sum(
            size(subdir, dirs) for subdir in dirs[d]["subdirs"]
        )
    return dirs[d]["total_size"]


def compute1(fname):
    dirs = parse_listing(fname)
    size("/", dirs)
    return sum(d["total_size"] for d in dirs.values() if d["total_size"] < 100000)


def compute2(fname):
    dirs = parse_listing(fname)
    used = size("/", dirs)
    capacity = 70000000
    unused = capacity - used
    needed = 30000000 - unused
    return min(d["total_size"] for d in dirs.values() if d["total_size"] > needed)


def test_compute1():
    assert compute1("test.txt") == 95437


def test_compute2():
    assert compute2("test.txt") == 24933642


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
