import unittest

from algorithm import graph
from ..util import load_graph_from_file

_data_path = f"{graph.__path__[0]}/tests/data"


class BfsTest(unittest.TestCase):
    def test_load_graph_from_file(self):
        g = load_graph_from_file(f"{_data_path}/graph_001.txt")
        self.assertEqual(len(g.vertices), 9)
        self.assertEqual(set(g.vertices), {"A", "B", "C", "D", "E", "F", "G", "H", "I"})
        self.assertEqual([(e.u, e.v, e.weight) for e in sorted(g.edges(), key=lambda e: f'{e.u}->{e.v}')], [
            ("A", "B", 1.0),
            ("A", "D", 1.0),
            ("A", "I", 1.0),
            ("B", "A", 1.0),
            ("B", "H", 1.0),
            ("C", "D", 1.0),
            ("C", "F", 1.0),
            ("C", "H", 1.0),
            ("D", "A", 1.0),
            ("D", "C", 1.0),
            ("D", "E", 1.0),
            ("E", "D", 1.0),
            ("E", "I", 1.0),
            ("F", "C", 1.0),
            ("F", "G", 1.0),
            ("G", "F", 1.0),
            ("H", "B", 1.0),
            ("H", "C", 1.0),
            ("I", "A", 1.0),
            ("I", "E", 1.0),
        ])


if __name__ == '__main__':
    unittest.main()
