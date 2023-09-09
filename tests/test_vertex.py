import unittest
import sys

sys.path.append("../")
from graphx import Vertex


class VertexTest(unittest.TestCase):
    def test_vertex1(self):
        v1 = Vertex(1)

        self.assertEqual(v1.values(), 1)

        v2 = Vertex("ok")

        self.assertEqual(v2.values(), "ok")
