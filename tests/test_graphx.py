import unittest

import sys

sys.path.append("../")

from graphx import GraphX
from tests.dummy import (
    generate_test_entities_num,
    generate_test_entities_person,
    Person,
)


class GraphXTest(unittest.TestCase):
    def test_nodes1(self):
        vals = generate_test_entities_num()
        gx = GraphX()
        gx.add_nodes(vals)
        expected = gx.nodes()
        self.assertEqual(expected, vals)
        val = 3
        with self.assertRaises(ValueError):
            gx.add_node(val)

    def test_nodes2(self):
        vals = generate_test_entities_person()
        gx = GraphX()
        gx.add_nodes(vals)
        expected = gx.nodes()
        self.assertEqual(expected, vals)

        val = Person("1", 1)
        with self.assertRaises(ValueError):
            gx.add_node(val)

    def test_edge1(self):
        vals = generate_test_entities_num()
        gx = GraphX()
        gx.add_nodes(vals)
        relationship1 = {"from": vals[0], "to": vals[1], "forward": "out"}
        gx.add_edge(relationship1)

        v1 = gx._vertex(vals[0])
        v2 = gx._vertex(vals[1])
        exist = v1.contains(v2, "to", "out")
        self.assertTrue(exist, True)

    def test_edge2(self):
        vals = generate_test_entities_person()
        gx = GraphX()
        gx.add_nodes(vals)

        relationship1 = {"from": vals[0], "to": vals[1], "forward": "out"}
        relationship2 = {
            "from": vals[1],
            "to": vals[2],
            "forward": "dumb",
            "backward": "smart",
        }
        edges = [relationship1, relationship2]
        gx.add_edges(edges)
        v0 = gx._vertex(vals[0])
        v1 = gx._vertex(vals[1])
        v2 = gx._vertex(vals[2])

        exist0 = v0.contains(v1, "to", "out")
        self.assertTrue(exist0, True)
        exist1 = v1.contains(v2, "to", "dumb")
        self.assertTrue(exist1, True)
        exist2 = v2.contains(v1, "from", "smart")
        self.assertTrue(exist2, True)
