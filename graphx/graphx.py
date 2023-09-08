from .entities import Vertex, Edge
import copy
from typing import Dict, List


# graph data structure
class GraphX:
    @classmethod
    def _copy(cls, objects: List) -> List:
        copies = []
        for obj in objects:
            copied = copy.deepcopy(obj)
            copies.append(copied)
        return copies

    def __init__(self, nodes=None, edges=None) -> None:
        """
        user should know nothing about the vertex/edge class
        instead they should pass in a dict of values for nodes
        and a dict of relationships for edges
        inside the GraphX class it will initiate the instances for nodes and edges
        but the edge should contain at least 3 keys, "from", "to", and "forward", and optional "backward"
        """
        self._nodes = []
        self._edges = []
        # for easier getting nodes
        # UUID vs Node dict
        self._nodes_lookup_map = {}

        # will call the add function, which will construct the vertex and edges
        if nodes is not None:
            # self._nodes = GraphX._copy(nodes)
            pass
        if edges is not None:
            # self._edges = GraphX._copy(edges)
            pass

    # return a copy of the stored nodes
    def nodes(self) -> List:
        return GraphX._copy(self._nodes)

    # return a copy of the stored edges
    def edges(self) -> List:
        return GraphX._copy(self._edges)

    def add_node(self, value):
        vertex = Vertex(value)
        if vertex in self._nodes_lookup_map.values():
            raise ValueError(f"vertex with value={vertex.value()} already exists")
        id = vertex.id()
        self._nodes_lookup_map[id] = vertex
        self._nodes.append(vertex)

    def add_nodes(self, values: List):
        for value in values:
            self.add_node(value)

    def add_edge(self, src_val, dest_val):
        pass
