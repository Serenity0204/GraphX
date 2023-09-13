import unittest
import sys

sys.path.append("../")
from graphx import GraphX
from tests.dummy import *


DEBUG = False


# nodes and edges
"""

nodes = [1, 2, 3, 4, 5, 6]


edges = [

    {"from": 1, "to": 2, "forward": "son"},

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


class GraphXTest(unittest.TestCase):
    def setUp(self):
        self.debug = DEBUG
        self.graphX = GraphX(nodes, edges)

    # debug print

    def print(self, result, name):
        if self.debug:
            print("from:" + name)

            print(result)

            print()

    def test_grandkids(self):
        nodes = self.graphX.query().node(1).forward().forward().run()

        self.print(nodes, self.test_grandkids.__name__)

        self.assertEqual(nodes, [3, 4, 5, 6])

    def test_sons_father(self):
        nodes = self.graphX.query().node(1).forward().backward().forward().run()

        self.print(nodes, self.test_sons_father.__name__)

        self.assertEqual(nodes, [2])

    def test_grandgrand_unique(self):
        # 3 4 5 6

        # 3: 4 5 6
        # 4: 3 5 6
        # 5: 4 3 6
        # 6: 3 4 5
        ## should be 4 5 6 3 5 6 4 3 6 3 4 5 -> 4 5 6 3
        nodes = self.graphX.query().node(1).forward().forward().forward().unique().run()

        self.print(nodes, self.test_grandgrand_unique.__name__)
        self.assertEqual(nodes, [4, 5, 6, 3])

    def test_take(self):
        nodes = (
            self.graphX.query()
            .node(1)
            .forward()
            .forward()
            .forward()
            .unique()
            .take(3)
            .run()
        )
        self.print(nodes, self.test_take.__name__)
        self.assertEqual(nodes, [4, 5, 6])

    def test_granddaughters(self):
        nodes = self.graphX.query().node(1).forward().forward(name_is="daughter").run()
        self.print(nodes, self.test_granddaughters.__name__)
        self.assertEqual(nodes, [6])

    def test_sisters(self):
        nodes = self.graphX.query().node(3).forward(name_is="sister").run()
        self.print(nodes, self.test_sisters.__name__)
        self.assertEqual(nodes, [6])

    def test_brothers_grandfater(self):
        # 4 5 6
        # 4b s: 2
        # 5b s: 2
        nodes = (
            self.graphX.query()
            .node(3)
            .forward()
            .backward(name_is="son")
            .backward(name_is="son")
            .unique()
            .run()
        )
        self.print(nodes, self.test_brothers_grandfater.__name__)
        self.assertEqual(nodes, [1])

    def test_sisters_brother(self):
        nodes = (
            self.graphX.query()
            .node(3)
            .forward(name_is="sister")
            .forward(name_is="brother")
            .run()
        )
        self.print(nodes, self.test_sisters_brother.__name__)
        self.assertEqual(nodes, [3, 4, 5])

    def test_brothers_father_daughter_prefix(self):
        # brother father daughter
        # 4 5 6
        # 4b s: 2
        # 5b s: 2
        # output: 6

        nodes = (
            self.graphX.query()
            .node(3)
            .forward()
            .backward(name_is="son")
            .forward(name_startswith="daughter")
            .unique()
            .run()
        )
        self.print(nodes, self.test_brothers_father_daughter_prefix.__name__)
        self.assertEqual(nodes, [6])

    def test_grandgrand_unique_sort(self):
        # 3 4 5 6

        # 3: 4 5 6
        # 4: 3 5 6
        # 5: 4 3 6
        # 6: 3 4 5
        ## should be 4 5 6 3 5 6 4 3 6 3 4 5 -> 4 5 6 3 -> 3, 4, 5, 6,
        nodes = (
            self.graphX.query()
            .node(1)
            .forward()
            .forward()
            .forward()
            .unique()
            .sort()
            .run()
        )

        self.print(nodes, self.test_grandgrand_unique_sort.__name__)
        self.assertEqual(nodes, [3, 4, 5, 6])

    def test_grandgrand_unique_filter(self):
        # 3 4 5 6

        # 3: 4 5 6
        # 4: 3 5 6
        # 5: 4 3 6
        # 6: 3 4 5
        ## should be 4 5 6 3 5 6 4 3 6 3 4 5 -> 4 5 6 3 -> 3, 4, 5, 6,
        nodes = (
            self.graphX.query()
            .node(1)
            .forward()
            .forward()
            .forward()
            .unique()
            .filter(3)
            .run()
        )

        self.print(nodes, self.test_grandgrand_unique_filter.__name__)
        self.assertEqual(nodes, [3])

    def test_grandgrand_unique_exclude(self):
        # 3 4 5 6

        # 3: 4 5 6
        # 4: 3 5 6
        # 5: 4 3 6
        # 6: 3 4 5
        ## should be 4 5 6 3 5 6 4 3 6 3 4 5 -> 4 5 6 3 -> 3, 4, 5, 6,
        nodes = (
            self.graphX.query()
            .node(1)
            .forward()
            .forward()
            .forward()
            .unique()
            .exclude(5)
            .sort()
            .run()
        )

        self.print(nodes, self.test_grandgrand_unique_exclude.__name__)
        self.assertEqual(nodes, [3, 4, 6])

    def test_grandgrand_exclude_unique(self):
        nodes = (
            self.graphX.query()
            .node(1)
            .forward()
            .forward()
            .forward()
            .exclude(5, 4, 6)
            .unique()
            .sort()
            .run()
        )

        self.print(nodes, self.test_grandgrand_unique_exclude.__name__)
        self.assertEqual(nodes, [3])
