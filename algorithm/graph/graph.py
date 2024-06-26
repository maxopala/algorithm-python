class Edge:
    def __init__(self, u: str, v: str, weight: float = 1.0):
        self.u = u
        self.v = v
        self.weight = weight

    def __str__(self):
        return f'{self.u}-({self.weight})->{self.v}'


class Graph:
    def __init__(self, vertices_ids: list[str] = None, vertices_count: int = None):
        self.vertices: dict[str, dict[str, float]] = {}
        if vertices_ids is not None and len(vertices_ids) > 0:
            for u in vertices_ids:
                self.add_vertex(vertex_id=u)
        elif vertices_count is not None and vertices_count > 0:
            for i in range(vertices_count):
                self.add_vertex(vertex_id=str(i))

    def add_vertex(self, vertex_id: str = None) -> None:
        if vertex_id is None:
            vertex_id = len(self.vertices)
            while vertex_id in self.vertices:
                vertex_id += 1
        if vertex_id in self.vertices:
            raise ValueError(f'Vertex {vertex_id} already exists')
        self.vertices[vertex_id] = {}

    def add_edge(self, u: str, v: str, weight: float = 1.0, bidirectional=False,
                 create_vertex_if_not_exists=False) -> None:
        if u not in self.vertices:
            if not create_vertex_if_not_exists:
                raise ValueError(f'Vertex {u} does not exist')
            self.add_vertex(vertex_id=u)

        if v not in self.vertices:
            if not create_vertex_if_not_exists:
                raise ValueError(f'Vertex {v} does not exist')
            self.add_vertex(vertex_id=v)

        self.vertices[u][v] = weight
        if bidirectional:
            self.vertices[v][u] = weight

    def neighbors(self, u: str) -> list[Edge]:
        return [Edge(u, v, self.vertices[u][v]) for v in sorted(self.vertices[u])]

    def edges(self) -> list[Edge]:
        edges = []
        for u in sorted(self.vertices):
            edges += self.neighbors(u)
        return edges

    def transpose(self) -> "Graph":
        g_t = Graph()
        for e in self.edges():
            g_t.add_edge(e.v, e.u, e.weight, create_vertex_if_not_exists=True)
        return g_t
