from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Callable, Generic, Self, TypeVar

T = TypeVar("T")
Edge = tuple[int, T]
GraphFunction = Callable[[T], set[Edge[T]]]


# The objects we put on the pq in Dijkstra. These are sortable dataclasses
# rather than naive (distance, node) tuples because the objects in the pq must
# be sortable and node objcts are not in general sortable.
@dataclass(frozen=True)
class NodeDistance(Generic[T]):
    dist: int
    node: T

    def __lt__(self, other: Self) -> bool:
        return self.dist < other.dist


def dijkstra(start: T, dest: T, g: GraphFunction[T]) -> int:
    distances: dict[T, int] = {start: 0}
    pq: list[NodeDistance[T]] = [NodeDistance(0, start)]

    while pq:
        nd = heappop(pq)
        node = nd.node
        d = nd.dist
        if d > distances[node]:
            continue

        # If we reach destination and the node at the front of the pq (i.e.
        # the closest node to start in the queue) is further from start than
        # dest then further work cannot possibly improve the path to dest.
        if node == dest and pq and pq[0].dist > d:
            break

        for edge_len, neighbor in g(node):
            new_dist = d + edge_len
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, NodeDistance(new_dist, neighbor))

    return distances[dest]


def build_paths(
    predecessors: dict[T, set[T]],
    start: T,
    dest: T,
) -> list[list[T]]:
    if dest == start:
        return [[start]]
    paths = []
    for pred in predecessors[dest]:
        for path in build_paths(predecessors, start, pred):
            paths.append(path + [dest])
    return paths


def dijkstra_all_paths(
    start: T,
    dest: T,
    g: GraphFunction[T],
) -> tuple[int | None, list[list[T]]]:
    """
    Returns the shortest distance from start to end and a list of _all_ paths
    from start to end that have that distance.
    """
    distances: dict[T, int] = {start: 0}
    predecessors: dict[T, set[T]] = {}
    pq: list[NodeDistance[T]] = [NodeDistance(0, start)]

    while pq:
        nd = heappop(pq)
        node = nd.node
        d = nd.dist

        if d > distances[node]:
            continue

        if node == dest and pq and pq[0].dist > d:
            break

        for edge_len, neighbor in g(node):
            new_dist = d + edge_len
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = {node}
                heappush(pq, NodeDistance(new_dist, neighbor))
            elif new_dist == distances[neighbor]:
                predecessors[neighbor].add(node)

    if dest not in distances:
        return None, []

    return distances[dest], build_paths(predecessors, start, dest)
