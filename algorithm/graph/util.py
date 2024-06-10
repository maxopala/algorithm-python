from collections import defaultdict

from .graph import Graph, Edge


def load_graph_from_file(file) -> Graph:
    edges: dict[str, list[Edge]] = defaultdict(list[Edge])
    with open(file) as f:
        for line in f:
            if line is not None:
                line = line.strip()
                if line.find("<->") >= 0:
                    parts = line.split("<->")
                    edges[parts[0].strip()].append(Edge(parts[0].strip(), parts[1].strip(), 1.0))
                    edges[parts[1].strip()].append(Edge(parts[1].strip(), parts[0].strip(), 1.0))
                elif line.find("<-(") >= 0 and line.find(")->") >= 0:
                    a = line.find("<-(")
                    b = line.find(")->") + 3
                    parts = [line[:a], line[a + 3:b - 3], line[b:]]
                    edges[parts[0].strip()].append(Edge(parts[0].strip(), parts[2].strip(), float(parts[1].strip())))
                    edges[parts[2].strip()].append(Edge(parts[2].strip(), parts[0].strip(), float(parts[1].strip())))
                elif line.find("-(") >= 0 and line.find(")->") >= 0:
                    a = line.find("-(")
                    b = line.find(")->") + 3
                    parts = [line[:a], line[a + 2:b - 3], line[b:]]
                    edges[parts[0].strip()].append(Edge(parts[0].strip(), parts[2].strip(), float(parts[1].strip())))
                elif line.find("->") >= 0:
                    parts = line.split("->")
                    edges[parts[0].strip()].append(Edge(parts[0].strip(), parts[1].strip(), 1.0))
    graph = Graph(vertices_ids=list(edges.keys()))
    for u in edges:
        for edge in edges[u]:
            graph.add_edge(edge.u, edge.v, edge.weight)
    return graph


def tree_as_str(graph, predecessor, vertex_info_function=None):
    d = {"tree": ""}
    for u in graph.vertices:
        if predecessor[u] == u:
            _tree_as_str_rec(graph, predecessor, vertex_info_function, u, d, "", None)
    return d["tree"]


def _tree_as_str_rec(graph, predecessor, vertex_info_function, u, d, before, last_child):
    if last_child is None:
        line = f"{u}"
        before = f""
    elif last_child:
        line = f"{before}└─>{u}"
        before = f"{before}   "
    else:
        line = f"{before}├─>{u}"
        before = f"{before}|  "
    if vertex_info_function is not None:
        line = f"{line} ({vertex_info_function(u)})"
    d["tree"] += f"{line}\n"
    children = [
        e.v for e in graph.neighbors(u) if predecessor[e.v] == u
    ]
    for i, v in enumerate(children):
        _tree_as_str_rec(graph, predecessor, vertex_info_function, v, d, before, i == len(children) - 1)
