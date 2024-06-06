import unittest

import graph
from .bfs import bfs_algorithm
from .kruskal import kruskal_algorithm
from .util import load_graph_from_file


class GraphTest(unittest.TestCase):
    def test_load_graph_from_file(self):
        g = load_graph_from_file(f"{graph.__path__[0]}/data/graph_001.txt")
        print(g.__dict__)
        # self.assertEqual(True, False)  # add assertion here

    def test_bfs_algorithm(self):
        g = load_graph_from_file(f"{graph.__path__[0]}/data/graph_001.txt")
        resp = bfs_algorithm(g, "A")
        for u in resp.visited:
            v = resp.visited[u]
            d = resp.distance[u]
            p = resp.predecessor[u]
            print(f"vertex {u} -> visited: {v} | distance: {d:.2f} | predecessor: {p}")

    def test_kruskal_algorithm(self):
        g = load_graph_from_file(f"{graph.__path__[0]}/data/graph_002.txt")
        resp = kruskal_algorithm(g)
        for edge in resp.tree_edges:
            print(f"{edge.u}<-({edge.weight})->{edge.v}")


if __name__ == '__main__':
    unittest.main()
