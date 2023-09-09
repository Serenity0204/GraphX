from .vertex import Vertex
from typing import Dict, List
from .utils import copy_list
import copy


# graph data structure
class Graph:
    def __init__(self) -> None:
        """
        user should know nothing about the vertex/edge class
        instead they should pass in a list of values for nodes
        and a dict of relationships for edges
        inside the GraphX class it will initiate the instances for nodes and edges
        but the edge should contain at least 3 keys, "from", "to", and optional "forward" and "backward" for custom names
        """
        self._nodes = []

    # return a copy of the stored nodes values
    def nodes(self) -> List:
        vertices = copy_list(self._nodes)
        vals = []
        for vertex in vertices:
            vals.append(copy.deepcopy(vertex.values()))
        return vals

    def add_node(self, value) -> None:
        vertex = Vertex(value)
        # cannot add duplicate
        if vertex in self._nodes:
            raise ValueError(f"vertex with value={vertex.values()} already exists")

        self._nodes.append(vertex)

    def add_nodes(self, values: List) -> None:
        for value in values:
            self.add_node(value)

    def add_edge(self, relationship: Dict) -> None:
        # contruct temp vertex, and check if vertex exists
        from_val = relationship.get("from", None)
        to_val = relationship.get("to", None)
        # if DNE then raise error
        if from_val is None or to_val is None:
            raise KeyError(f"required 'from' and 'to' as keys, but did not find")

        ## construct the dummy
        dummy_from = Vertex(from_val)
        dummy_to = Vertex(to_val)

        # get the stored vertex indices by dummy
        from_vertex_idx = self._nodes.index(dummy_from)
        to_vertex_idx = self._nodes.index(dummy_to)

        # get the actual vertices
        from_vertex = self._nodes[from_vertex_idx]
        to_vertex = self._nodes[to_vertex_idx]

        # get the name
        forward_name = relationship.get("forward", "forward")
        backward_name = relationship.get("backward", None)

        # update vertex
        from_vertex.add_to(to_vertex, forward_name)
        to_vertex.add_from(from_vertex, forward_name)

        if backward_name is not None:
            to_vertex.add_to(from_vertex, backward_name)
            from_vertex.add_from(to_vertex, backward_name)

    def add_edges(self, relationships: List[Dict]) -> None:
        for relationship in relationships:
            self.add_edge(relationship)

    def vertex(self, value) -> Vertex:
        vertex = Vertex(value)
        if vertex not in self._nodes:
            raise ValueError(f"vertex with value={value} cannot be found")
        idx = self._nodes.index(vertex)
        return copy.copy(self._nodes[idx])
