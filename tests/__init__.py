import unittest

from .test_graph import GraphTest
from .test_pipe import PipeTest
from .test_query import QueryTest
from .test_vertex import VertexTest
from .dummy import *


def main():
    unittest.main(__name__)


if __name__ == "__main__":
    main()
