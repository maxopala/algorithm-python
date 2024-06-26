from collections import defaultdict
from enum import Enum

from .graph import Graph
from .util import tree_as_str


class DfsEdgeType(str, Enum):
    TREE = 'TREE'
    RETURN = 'RETURN'
    DIRECT = 'DIRECT'
    CROSS = 'CROSS'


class DfsResult:
    def __init__(self, **kv):
        self.graph = kv["graph"]
        self.start_instant = kv["start_instant"]
        self.finish_instant = kv["finish_instant"]
        self.predecessor = kv["predecessor"]

    def vertices_topological_sorted(self) -> list[str]:
        return [
            f[0] for f in sorted(self.finish_instant.items(), key=lambda x: x[1], reverse=True)
        ]

    def tree_as_str(self):
        return tree_as_str(self.graph, self.predecessor, lambda u: f"{self.start_instant[u]}/{self.finish_instant[u]}")


def _next_vertex(graph: Graph, visited, start_order):
    if start_order is not None:
        for u in start_order:
            if not visited[u]:
                return u
    for u in sorted(graph.vertices):
        if not visited[u]:
            return u
    return None


def _dfs_algorithm_rec(graph: Graph, u: str, data):
    data["instant"] += 1
    data["visited"][u] = True
    data["start_instant"][u] = data["instant"]
    for edge in graph.neighbors(u):
        if not data["visited"][edge.v]:
            data["predecessor"][edge.v] = u
            _dfs_algorithm_rec(graph, edge.v, data)
    data["instant"] += 1
    data["finish_instant"][u] = data["instant"]
    data["finished_count"] -= 1


def dfs_algorithm(graph: Graph, start_order: list[str] = None) -> DfsResult:
    data = {
        "visited": {u: False for u in sorted(graph.vertices)},
        "start_instant": {u: -1 for u in sorted(graph.vertices)},
        "finish_instant": {u: -1 for u in sorted(graph.vertices)},
        "predecessor": {u: "" for u in sorted(graph.vertices)},
        "finished_count": len(graph.vertices),
        "instant": 0
    }

    while data["finished_count"] > 0:
        u = _next_vertex(graph, data["visited"], start_order)
        data["predecessor"][u] = u
        _dfs_algorithm_rec(graph, u, data)

    return DfsResult(
        graph=graph,
        start_instant=data["start_instant"],
        finish_instant=data["finish_instant"],
        predecessor=data["predecessor"]
    )


def strongly_connected_components(dfs_result: DfsResult) -> list[set[str]]:
    graph = dfs_result.graph.transpose()
    result = dfs_algorithm(graph, dfs_result.vertices_topological_sorted())
    components = []
    for u in sorted(graph.vertices):
        if result.predecessor[u] == u:
            queue = [u]
            c = {u}
            while queue:
                w = queue.pop(0)
                for e in graph.neighbors(w):
                    if result.predecessor[e.v] == w and e.v not in c:
                        c.add(e.v)
                        queue.append(e.v)
            components.append(c)
    return components


def classify_dfs_edges(dfs_result: DfsResult) -> dict[str, dict[str, DfsEdgeType]]:
    graph = dfs_result.graph
    predecessor = dfs_result.predecessor
    finish_instant = dfs_result.finish_instant
    classify: dict[str, dict[str, DfsEdgeType]] = defaultdict(dict[str, DfsEdgeType])
    for e in graph.edges():
        if predecessor[e.v] == e.u:
            classify[e.u][e.v] = DfsEdgeType.TREE
        elif predecessor[e.u] == e.v:
            classify[e.u][e.v] = DfsEdgeType.RETURN
        elif finish_instant[e.u] > finish_instant[e.v]:
            classify[e.u][e.v] = DfsEdgeType.DIRECT
        else:
            classify[e.u][e.v] = DfsEdgeType.CROSS
    return classify
