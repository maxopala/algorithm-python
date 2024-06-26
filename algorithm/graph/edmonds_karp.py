from math import inf

from .graph import Graph


class EdmondsKarpPath:
    def __init__(self, **kv):
        self.path: list[str] = kv["path"]
        self.flow = kv["flow"]

    def pretty_str(self):
        return f"Flow value: {self.flow} | Path: {'->'.join(self.path)}"


class EdmondsKarpResult:
    def __init__(self, **kv):
        self.graph = kv["graph"]
        self.work_graph = kv["work_graph"]
        self.paths = kv["paths"]

    def total_flow(self):
        total = 0
        for path in self.paths:
            total += path.flow
        return total

    def pretty_str(self):
        return '\n'.join(
            [path.pretty_str() for path in self.paths] + [f'Total flow: {self.total_flow()}']
        )


def edmonds_karp_algorithm(graph: Graph):
    work_graph = Graph(vertices_ids=list(graph.vertices.keys()))
    for edge in graph.edges():
        work_graph.add_edge(edge.u, edge.v, edge.weight)
        if edge.u not in graph.vertices[edge.v]:
            work_graph.add_edge(edge.v, edge.u, 0)

    result = EdmondsKarpResult(
        graph=graph,
        work_graph=work_graph,
        paths=[],
    )

    return result


def edmonds_karp_algorithm_step(result: EdmondsKarpResult, path: list):
    g = result.work_graph
    flow = inf
    for u, v in zip(path[:-1], path[1:]):
        if v not in g.vertices[u]:
            return False
        value = g.vertices[u][v]
        if value < flow:
            flow = value
    if flow <= 0 or flow == inf:
        return False
    for u, v in zip(path[:-1], path[1:]):
        g.vertices[u][v] -= flow
        g.vertices[v][u] += flow
    result.paths.append(EdmondsKarpPath(path=path, flow=flow))
    return True
