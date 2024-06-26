import unittest

from algorithm import graph
from ..bfs import bfs_algorithm
from ..dfs import dfs_algorithm, strongly_connected_components
from ..kruskal import kruskal_algorithm
from ..util import load_graph_from_file

_data_path = f"{graph.__path__[0]}/tests/data"


class BfsTest(unittest.TestCase):
    def test_bfs_algorithm(self):
        g = load_graph_from_file(f"{_data_path}/graph_004.txt")
        resp = bfs_algorithm(g, "e")
        print(resp.tree_as_str())
        for u in resp.visited:
            v = resp.visited[u]
            d = resp.distance[u]
            p = resp.predecessor[u]
            print(f"vertex {u} -> visited: {v} | distance: {d:.2f} | predecessor: {p}")

    def test_dfs_algorithm(self):
        g = load_graph_from_file(f"{_data_path}/graph_004.txt")
        resp = dfs_algorithm(g)
        print(resp.tree_as_str())
        for u in g.vertices:
            s = resp.start_instant[u]
            f = resp.finish_instant[u]
            p = resp.predecessor[u]
            print(f"vertex {u} -> start: {s} | finish: {f:.2f} | predecessor: {p}")

    def test_strongly_connected_components(self):
        g = load_graph_from_file(f"{_data_path}/graph_004.txt")
        resp = dfs_algorithm(g)
        components = strongly_connected_components(resp)
        print(components)

    def test_kruskal_algorithm(self):
        g = load_graph_from_file(f"{_data_path}/graph_002.txt")
        resp = kruskal_algorithm(g)
        for edge in resp.tree_edges:
            print(f"{edge.u}<-({edge.weight})->{edge.v}")


if __name__ == '__main__':
    unittest.main()
