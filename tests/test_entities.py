import unittest

import sys


sys.path.append("../")

from graphx import Edge, Vertex, GraphX


class EntitiesTest(unittest.TestCase):
    def test_vertex1(self):
        v1 = Vertex(1)

        self.assertEqual(v1.get(), 1)

        v2 = Vertex("ok")

        self.assertEqual(v2.get(), "ok")

    def test_edge1(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        e1 = Edge(v1, v2, "hello")
        self.assertEqual(e1.get_forward_info(), {"from": v1, "to": v2, "name": "hello"})

        v3 = Vertex(3)
        v4 = Vertex(4)
        e2 = Edge(v3, v4, "out", "in", True)
        self.assertEqual(e2.get_forward_info(), {"from": v3, "to": v4, "name": "out"})
        self.assertEqual(e2.get_backward_info(), {"from": v4, "to": v3, "name": "in"})
