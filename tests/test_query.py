import unittest
import sys

sys.path.append("../")
from graphx import Query, Graph, Vertex
from tests.dummy import *


DEBUG = False


# nodes and edges
"""

nodes = [1, 2, 3, 4, 5, 6]


edges = [

    {"from": 1, "to": 2, "forward": "son", "backward": "father"},

    {"from": 2, "to": 3, "forward": "son"},

    {"from": 2, "to": 4, "forward": "son"},

    {"from": 2, "to": 5, "forward": "son"},

    {"from": 2, "to": 6, "forward": "daughter"},

    {"from": 3, "to": 4, "forward": "brother", "backward": "brother"},

    {"from": 4, "to": 5, "forward": "brother", "backward": "brother"},

    {"from": 5, "to": 3, "forward": "brother", "backward": "brother"},

    {"from": 3, "to": 6, "forward": "sister", "backward": "brother"},

    {"from": 4, "to": 6, "forward": "sister", "backward": "brother"},

    {"from": 5, "to": 6, "forward": "sister", "backward": "brother"},

]

"""


class QueryTest(unittest.TestCase):
    def setUp(self):
        self.debug = DEBUG

        g = Graph()

        g.add_nodes(nodes)

        g.add_edges(edges)

        self.q = Query(g)

    # debug print

    def print(self, result, name):
        if self.debug:
            print("from:" + name)

            print(result)

            print()

    def test_grandkids(self):
        nodes = self.q.node(1).forward().forward().run()

        self.print(nodes, self.test_grandkids.__name__)

        self.assertEqual(nodes, [3, 4, 5, 6])

    def test_sons_father(self):
        nodes = self.q.node(1).forward().backward().forward().run()

        self.print(nodes, self.test_sons_father.__name__)

        self.assertEqual(nodes, [2])

    def test_grandgrand_unique(self):
        # 3 4 5 6

        # 4 6 5 6 3 6

        nodes = self.q.node(1).forward().forward().forward().unique().run()

        self.print(nodes, self.test_grandgrand_unique.__name__)
        self.assertEqual(nodes, [4, 5, 6, 3])

    def test_take(self):
        nodes = self.q.node(1).forward().forward().forward().unique().take(3).run()
        self.print(nodes, self.test_take.__name__)
        self.assertEqual(nodes, [4, 5, 6])

    # def test_toms_sisters(self):

    #     nodes = self.q.node(3).outcome("sister").run()

    #     self.assert_nodes(nodes, [6])

    # def test_toms_brothers_grandfater(self):

    #     nodes = self.q.node(3).outcome().income("son").income("son").run()

    #     self.assert_nodes(nodes, [1])

    # def test_grandfater_unique(self):

    #     nodes = self.q.node(3).outcome().income("son").income("son").unique().run()

    #     self.assertEqual(1, len(nodes))

    #     self.assertEqual(1, Dagoba.pk(nodes[0]))

    # def test_toms_sisters_brother(self):

    #     nodes = self.q.node(3).outcome("sister").outcome("brother").run()

    #     self.assert_nodes(nodes, [3, 4, 5])

    # def test_node_visits(self):

    #     self.db.reset_visits()

    #     eager_query = self.db.query(eager=True)

    #     eager_query.node(1).outcome("son").outcome("son").take(1).run()

    #     eager_visits = self.db.node_visits()

    #     self.db.reset_visits()

    #     lazy_query = self.db.query(eager=False)

    #     lazy_query.node(1).outcome("son").outcome("son").take(1).run()

    #     lazy_visits = self.db.node_visits()

    #     self.assertTrue(lazy_visits < eager_visits)

    # def test_custom_pipeline_grandkids(self):

    #     def grandkids(self_):

    #         self_.outcome().outcome()
    #         return self_

    #     LazyQuery.grandkids = grandkids

    #     nodes = self.q.node(1).grandkids().run()

    #     self.assert_nodes(nodes, [3, 4, 5, 6])
