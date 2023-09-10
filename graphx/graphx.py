from .pipe import Pipe
from .query import Query
from .vertex import Vertex
from .utils import *
from .graph import Graph
from typing import Dict, List
import copy


class GraphX:
    def __init__(self, nodes: List = None, edges: Dict = None) -> None:
        self._graph = Graph()
        self._query = Query(self._graph)
        if len(nodes) != 0:
            self.add_nodes(nodes)
        if len(edges) != 0:
            self.add_edges(edges)

    def add_node(self, value) -> None:
        self._graph.add_node(value)

    def add_nodes(self, values: List) -> None:
        self._graph.add_nodes(values)

    def add_edge(self, relationship: Dict) -> None:
        self._graph.add_edge(relationship)

    def add_edges(self, relationships: List[Dict]) -> None:
        self._graph.add_edges(relationships)

    def nodes(self) -> List:
        return self._graph.nodes()

    def query(self) -> Query:
        return self._query
