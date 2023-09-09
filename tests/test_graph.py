import unittest
import sys

sys.path.append("../")
from graphx import Graph
from tests.dummy import *


class GraphTest(unittest.TestCase):
    def test_nodes1(self):
        vals = generate_test_num()
        g = Graph()
        g.add_nodes(vals)
        expected = g.nodes()
        self.assertEqual(expected, vals)
        val = 3
        with self.assertRaises(ValueError):
            g.add_node(val)

    def test_nodes2(self):
        vals = generate_test_person(4)
        g = Graph()
        g.add_nodes(vals)
        expected = g.nodes()
        self.assertEqual(expected, vals)

        val = Person("1", 1)
        with self.assertRaises(ValueError):
            g.add_node(val)

    def test_edge1(self):
        vals = generate_test_num()
        g = Graph()
        g.add_nodes(vals)
        relationship1 = {"from": vals[0], "to": vals[1], "forward": "out"}
        g.add_edge(relationship1)

        v1 = g.vertex(vals[0])
        v2 = g.vertex(vals[1])
        exist = v1.contains(v2, "to", "out")
        self.assertTrue(exist, True)

    def test_edge2(self):
        vals = generate_test_person(4)
        g = Graph()
        g.add_nodes(vals)

        relationship1 = {"from": vals[0], "to": vals[1], "forward": "out"}
        relationship2 = {
            "from": vals[1],
            "to": vals[2],
            "forward": "dumb",
            "backward": "smart",
        }
        edges = [relationship1, relationship2]
        g.add_edges(edges)
        v0 = g.vertex(vals[0])
        v1 = g.vertex(vals[1])
        v2 = g.vertex(vals[2])

        exist0 = v0.contains(v1, "to", "out")
        self.assertTrue(exist0, True)
        exist1 = v1.contains(v2, "to", "dumb")
        self.assertTrue(exist1, True)
        exist2 = v2.contains(v1, "from", "smart")
        self.assertTrue(exist2, True)
