from algorithm.graph import Graph


class KruskalResult:
    def __init__(self, **kv):
        self.graph = kv["graph"]
        self.tree_edges = kv["tree_edges"]


def kruskal_algorithm(graph: Graph) -> KruskalResult:
    edges = graph.edges()
    edges.sort(key=lambda e: e.weight)
    group = {u: i for i, u in enumerate(graph.vertices)}
    tree_edges = []

    for edge in edges:
        if group[edge.u] == group[edge.v]:
            continue
        tree_edges.append(edge)
        u_group = group[edge.u]
        v_group = group[edge.v]
        for k in graph.vertices:
            if group[k] == v_group:
                group[k] = u_group
        if len(tree_edges) == len(graph.vertices) - 1:
            break

    if len(tree_edges) < len(graph.vertices) - 1:
        raise ValueError("Sem árvore espalhada mínima")

    return KruskalResult(graph=graph, tree_edges=tree_edges)
