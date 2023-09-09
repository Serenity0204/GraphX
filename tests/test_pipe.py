import unittest
import sys

sys.path.append("../")
from graphx import Graph, Pipe, Vertex
from tests.dummy import *


class PipeTest(unittest.TestCase):
    def test_pipe1(self):
        vals = generate_test_person(4)

        g = Graph()

        g.add_nodes(vals)

        # get vertices to compare later

        expected = [g.vertex(vals[1]), g.vertex(vals[2])]

        relationship1 = {"from": vals[0], "to": vals[1], "forward": "out"}

        relationship2 = {
            "from": vals[0],
            "to": vals[2],
            "forward": "dumb",
            "backward": "smart",
        }

        edges = [relationship1, relationship2]

        g.add_edges(edges)

        arg = [g.vertex(vals[0])]

        p = Pipe("forward")

        pipe = p.function()

        check = pipe != None

        self.assertTrue(check)

        result = pipe(arg)

        self.assertEqual(expected, result)

    def test_pipe2(self):
        vals = generate_test_person(10)

        g = Graph()

        g.add_nodes(vals)

        relationships = []

        for i in range(0, 5):
            if i > 1:
                rel = {
                    "from": vals[1],
                    "to": vals[i],
                    "forward": "forwards",
                    "backward": "backwards",
                }

                relationships.append(rel)

            elif i == 0:
                rel = {"from": vals[i], "to": vals[i + 1], "forward": "forwards"}

                relationships.append(rel)

        g.add_edges(relationships)

        arg = [g.vertex(vals[0])]

        p = Pipe("forward")

        pipe = p.function()

        check = pipe != None

        self.assertTrue(check)
        result = pipe(arg)

        expected = [g.vertex(vals[1])]

        self.assertEqual(expected, result)

        arg = result

        p = Pipe("forward")
        pipe = p.function()
        result = pipe(arg)

        expected = [g.vertex(vals[2]), g.vertex(vals[3]), g.vertex(vals[4])]

        self.assertEqual(expected, result)

        arg = result

        p = Pipe("backward")
        pipe = p.function()
        result = pipe(arg)

        expected = [g.vertex(vals[1]), g.vertex(vals[1]), g.vertex(vals[1])]

        self.assertEqual(expected, result)

        arg = result

        p = Pipe("unique")
        pipe = p.function()
        result = pipe(arg)

        expected = [g.vertex(vals[1])]

        self.assertEqual(expected, result)
