from math import inf

from .util import tree_as_str
from .graph import Graph


class BfsResult:
    def __init__(self, **kv):
        self.graph = kv["graph"]
        self.start = kv["start"]
        self.visited = kv["visited"]
        self.distance = kv["distance"]
        self.predecessor = kv["predecessor"]

    def tree_as_str(self):
        return tree_as_str(self.graph, self.predecessor)


def bfs_algorithm(graph: Graph, start: str):
    visited = {u: False for u in graph.vertices}
    distance = {u: inf for u in graph.vertices}
    predecessor = {u: "" for u in graph.vertices}
    visited[start] = True
    distance[start] = 0
    predecessor[start] = start
    queue = [start]
    while queue:
        u = queue.pop(0)
        for edge in graph.neighbors(u):
            if not visited[edge.v]:
                visited[edge.v] = True
                distance[edge.v] = distance[u] + 1
                predecessor[edge.v] = u
                queue.append(edge.v)
    return BfsResult(
        graph=graph,
        start=start,
        visited=visited,
        distance=distance,
        predecessor=predecessor,
    )
