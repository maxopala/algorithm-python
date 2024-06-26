from math import inf

from .util import tree_as_str
from .graph import Graph


class DijkstraResult:
    def __init__(self, **kv):
        self.graph = kv["graph"]
        self.start = kv["start"]
        self.distance = kv["distance"]
        self.predecessor = kv["predecessor"]

    def tree_as_str(self):
        return tree_as_str(self.graph, self.predecessor)


def dijkstra_algorithm(graph: Graph, start: str):
    distance = {u: inf for u in sorted(graph.vertices)}
    predecessor = {u: "" for u in sorted(graph.vertices)}
    distance[start] = 0
    predecessor[start] = start
    queue = [start]

    def extract_vertex():
        queue.sort(key=lambda u: distance[u], reverse=True)
        return queue.pop()

    while queue:
        u = extract_vertex()
        for edge in graph.neighbors(u):
            if distance[u] + edge.weight < distance[edge.v]:
                distance[edge.v] = distance[u] + edge.weight
                predecessor[edge.v] = u
                queue.append(edge.v)
    return DijkstraResult(
        graph=graph,
        start=start,
        distance=distance,
        predecessor=predecessor,
    )
