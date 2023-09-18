import unittest
import sys

sys.path.append("../")
from graphx import GraphX, Query
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

    def test_forward_filter_sort(self):
        # 3 4 5 6 no 5 6

        # 3: 4 5 6
        # 4: 3 5 6
        # X 5: 4 3 6
        # X 6: 3 4 5
        ## should be 4 5 6 3 5 6  -> 3, 4, 5, 5, 6, 6
        nodes = (
            self.graphX.query()
            .node(1)
            .forward()
            .forward()
            .filter(3, 4)
            .forward()
            .sort()
            .run()
        )

        self.print(nodes, self.test_forward_filter_sort.__name__)
        self.assertEqual(nodes, [3, 4, 5, 5, 6, 6])

    def test_merge_forward_forward(self):
        nodes = (
            self.graphX.query()
            .node(1)
            .tag("self")
            .forward()
            .tag("son")
            .forward()
            .merge("son", "self")
            .sort()
            .run()
        )
        # 1
        # 2
        # 3, 4, 5, 6
        self.print(nodes, self.test_merge_forward_forward.__name__)

        self.assertEqual(nodes, [1, 2, 3, 4, 5, 6])

    def test_merge_forward_forward_no_son(self):
        nodes = (
            self.graphX.query()
            .node(1)
            .tag("self")
            .forward()
            .tag("son")
            .forward()
            .merge("self")
            .sort()
            .run()
        )
        # 1
        # 3, 4, 5, 6
        self.print(nodes, self.test_merge_forward_forward_no_son.__name__)

        self.assertEqual(nodes, [1, 3, 4, 5, 6])

    def test_forward_filter_merge(self):
        # 1
        # 2
        # 3 4 5 6 no 5 6

        # 3: 4 5 6
        # 4: 3 5 6
        # X 5: 4 3 6
        # X 6: 3 4 5
        ## should be 4 5 6 3 5 6  -> 3, 4, 5, 5, 6, 6
        nodes = (
            self.graphX.query()
            .node(1)
            .tag("self")  # remember 1
            .forward()
            .tag("son")  # remember 2
            .forward()
            .tag("gs")  # remember 3, 4, 5, 6
            .filter(3, 4)  # remember 3, 4
            .tag("gs34")  ## here will be 3, 4 for outputs
            .merge("gs", "gs34", "son")  # merge 3, 4 with 3, 4, 5, 6, and 3, 4, and 2
            .run()
        )

        self.print(nodes, self.test_forward_filter_merge.__name__)
        self.assertEqual(nodes, [3, 4, 3, 4, 5, 6, 3, 4, 2])

    def test_custom_name(self):
        def grandson(_self):
            return _self.forward().forward()

        def nullcall(_self):
            return _self

        Query.add_alias("grandson", grandson)
        Query.add_alias("nullcall", nullcall)

        nodes = self.graphX.query().node(1).grandson().nullcall().run()

        self.print(nodes, self.test_custom_name.__name__)

        self.assertEqual(nodes, [3, 4, 5, 6])

    def test_tag_custom_filter_merge(self):
        def grandson(_self):
            return _self.forward().forward()

        Query.add_alias("grandson_here", grandson)
        nodes = (
            self.graphX.query()
            .node(1)
            .tag("self")  # remember 1
            .grandson_here()
            .tag("grandson")  # remember 3, 4, 5, 6
            .filter(3, 4)  ## here will be 3, 4 for outputs
            .merge("self", "grandson")  # merge 3, 4 with 1 and 3, 4, 5, 6
            .run()  # 3, 4, 1, 3, 4, 5, 6
        )

        self.print(nodes, self.test_tag_custom_filter_merge.__name__)
        self.assertEqual(nodes, [3, 4, 1, 3, 4, 5, 6])
