from .util import tree_as_str
from .graph import Graph


class DfsResult:
    def __init__(self, **kv):
        self.graph = kv["graph"]
        self.start_instant = kv["start_instant"]
        self.finish_instant = kv["finish_instant"]
        self.predecessor = kv["predecessor"]

    def tree_as_str(self):
        return tree_as_str(self.graph, self.predecessor, lambda u: f"{self.start_instant[u]}/{self.finish_instant[u]}")


def _next_vertex(graph: Graph, visited, start_order):
    if start_order is not None:
        for u in start_order:
            if visited[u]:
                return u
    for u in graph.vertices:
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
        "visited": {u: False for u in graph.vertices},
        "start_instant": {u: -1 for u in graph.vertices},
        "finish_instant": {u: -1 for u in graph.vertices},
        "predecessor": {u: "" for u in graph.vertices},
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
