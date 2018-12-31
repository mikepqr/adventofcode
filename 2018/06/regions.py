from collections import Counter


def load_points():
    points = {}
    with open("input.txt") as f:
        for point_id, line in enumerate(f):
            points[point_id] = tuple(map(int, line.split(",")))
    return points


def md(x1, y1, x2, y2):
    """
    Manhattan distance between two points.
    """
    return abs(x1 - x2) + abs(y1 - y2)


def nearest(x0, y0, points):
    """
    Return name of point in points closest to (x0, y0)
    """
    distances = {name: md(x0, y0, x, y) for name, (x, y) in points.items()}
    minimum_distance = min(distances.items(), key=lambda x: x[1])[1]
    nearest_points = [name for name, distance in distances.items()
                      if distance == minimum_distance]
    if len(nearest_points) == 1:
        return nearest_points[0]
    else:
        return False  # Tie


def grid_size(points):
    """
    Return largest x and y in points {name: (x,y)}
    """
    return (max(x for x, _ in points.values()),
            max(y for _, y in points.values()))


def largest_region(grid, maxx, maxy):
    """
    Return the name and size of the largest region in the grid that is not on
    its edge.
    """
    infinite_regions = set([name for (x, y), name in grid.items()
                            if x in {0, maxx} or y in {0, maxy}])
    return next((region, size)
                for region, size in Counter(grid.values()).most_common()
                if region not in infinite_regions)


def nearest_points_grid(points, maxx, maxy):
    """
    Construct grid {(x, y): nearest point} giving name of point nearest to
    location (x, y).
    """
    grid = {}
    for x in range(maxx + 1):
        for y in range(maxy + 1):
            nearest_point = nearest(x, y, points)
            if nearest_point:
                grid[(x, y)] = nearest_point
    return grid


def within_distance_grid(points, maxx, maxy, N=10000):
    """
    Construct grid {(x, y): boolean flag} where flag is True if the sum of the
    Manhattan distances from (x, y) to all points is < N.
    """
    grid = {}
    for x in range(maxx + 1):
        for y in range(maxy + 1):
            if sum(md(x, y, xp, yp) for (xp, yp) in points.values()) < N:
                grid[(x, y)] = True
            else:
                grid[(x, y)] = False
    return grid


def part1():
    points = load_points()
    maxx, maxy = grid_size(points)
    grid = nearest_points_grid(points, maxx, maxy)
    return largest_region(grid, maxx, maxy)


def part2():
    points = load_points()
    maxx, maxy = grid_size(points)
    grid = within_distance_grid(points, maxx, maxy)
    return sum(grid.values())
