from .pipe import Pipe
from .graph import Graph
from .vertex import Vertex
from .utils import *
from typing import List, Dict
import copy


class Query:
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self._initial: List[Vertex] = []

        # pipelines for storing functions, args for storing argument for corresponding function

        self._pipelines: List = []

        self._args = []

        # map of index of last pipe vs name , index = -1 for initial
        self._tags = {}

        # map of index of last pipe vs merge call names
        self._merges = {}

    # this does not make sense to be called in the middle way
    def node(self, value):
        if len(self._initial) > 0:
            raise RuntimeError("cannot call node in the midway of a chaining query")
        self._initial.append(self._graph.vertex(value))
        return self

    def clean(self) -> None:
        self._initial.clear()
        self._args.clear()
        self._tags.clear()
        self._merges.clear()

    def _query(self, name, *args) -> None:
        if len(self._initial) == 0:
            raise RuntimeError("cannot query if didn't call node(val) first")

        pipeline = Pipe(name)
        pipefunc = pipeline.function()

        arguments = [] if len(args) == 0 else list(args)
        self._pipelines.append(pipefunc)
        self._args.append(arguments)

    def run(self):
        if len(self._initial) == 0:
            raise RuntimeError("cannot query if didn't call node(val) first")

        # store history pipe outputs for tag/merge
        history = {}

        inputs, outputs = self._initial, None

        for i in range(0, len(self._pipelines)):
            pipefunc = self._pipelines[i]

            args = self._args[i]

            if len(args) == 0:
                outputs = pipefunc(inputs)
            else:
                outputs = pipefunc(inputs, *args)

            is_merged = False
            if i in self._tags:
                # copy output and put it into history, but only the tagged one
                ## get the tagged name
                name = self._tags[i]
                history_output = copy.copy(outputs)
                history[name] = history_output
            # if i in self._merges:
            #     self._merge(inputs, self._merges[i], history)

            # update inputs
            inputs = outputs
        results = []
        for vertex in outputs:
            results.append(copy.copy(vertex.values()))

        self.clean()
        return results

    # does not make sense to call if didn't call node first

    def forward(self, **kwargs):
        if len(kwargs) > 1:
            raise ValueError("invalid number of kwargs")

        query = decide_query(kwargs)
        name = kwargs.get(query, None)
        self._query("forward", query, name)
        return self

    def backward(self, **kwargs):
        if len(kwargs) > 1:
            raise ValueError("invalid number of kwargs")
        query = decide_query(kwargs)
        name = kwargs.get(query, None)
        self._query("backward", query, name)
        return self

    def unique(self):
        self._query("unique")
        return self

    def take(self, num: int):
        self._query("take", num)
        return self

    def filter(self, *args):
        self._query("filter", args)
        return self

    def exclude(self, *args):
        self._query("exclude", args)
        return self

    def sort(self, ascending=True):
        self._query("sort", ascending)
        return self

    # name has to be unique
    def tag(self, name: str):
        if name in self._tags.values():
            raise ValueError("name of tag cannot be duplicate")
        # if no pipes, then tag the initial
        if len(self._pipelines) == 0:
            self._tags[-1] = name
            return self

        # else tag the last pipe index
        self._tags[len(self._pipelines) - 1] = name
        return self

    ## merge into pre-existing args helper
    def _merge(self, args: List[Vertex], names: List, history: Dict):
        result = args.copy()
        for name in names:
            if name in history:
                result += history[name]
        return result

    def merge(self, *args):
        return self
