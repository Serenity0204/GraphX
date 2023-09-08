import unittest

import sys

sys.path.append("../")

from graphx import GraphX
from tests.utils import generate_test_entities_num, generate_test_entities_person


class GraphXTest(unittest.TestCase):
    def test_graphx_add_nodes1(self):
        vals = generate_test_entities_num()
        gx = GraphX()
        gx.add_nodes(vals)
        filtered_vals = []
        for node in gx.nodes():
            val = node.value()
            filtered_vals.append(val)
        self.assertEqual(filtered_vals, vals)

    def test_graphx_add_nodes2(self):
        vals = generate_test_entities_person()
        gx = GraphX()
        gx.add_nodes(vals)
        filtered_vals = []
        for node in gx.nodes():
            val = node.value()
            filtered_vals.append(val)
        # self.assertEqual(filtered_vals, vals)
        print(filtered_vals)
