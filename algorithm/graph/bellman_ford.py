from math import inf

from .util import tree_as_str
from .graph import Graph


class BellmanFordResult:
    def __init__(self, **kv):
        self.graph = kv["graph"]
        self.start = kv["start"]
        self.distance = kv["distance"]
        self.predecessor = kv["predecessor"]
        self.has_solution = kv["has_solution"]

    def tree_as_str(self):
        return tree_as_str(self.graph, self.predecessor)


def bellman_ford_algorithm(graph: Graph, start: str):
    distance = {u: inf for u in sorted(graph.vertices)}
    predecessor = {u: "" for u in sorted(graph.vertices)}
    distance[start] = 0
    predecessor[start] = start
    queue = [start]

    change = False
    for i in range(len(graph.vertices) + 1):
        change = False
        for u in graph.vertices:
            for edge in graph.neighbors(u):
                if distance[u] + edge.weight < distance[edge.v]:
                    distance[edge.v] = distance[u] + edge.weight
                    predecessor[edge.v] = u
                    queue.append(edge.v)
                    change = True
        if not change:
            break

    return BellmanFordResult(
        graph=graph,
        start=start,
        distance=distance,
        predecessor=predecessor,
        has_solution=not change
    )
