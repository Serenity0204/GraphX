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

        # map of index of last pipe vs merge call names (list of names)
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
        self._pipelines.clear()

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

        # if no pipelines
        if len(self._pipelines) == 0:
            results = []
            for vertex in self._initial:
                results.append(copy.copy(vertex.values()))
            self.clean()
            return results

        # store history pipe outputs for tag/merge
        history = {}

        inputs, outputs = self._initial, None
        # store the tag for node() if needed
        if -1 in self._tags:
            name = self._tags[-1]
            history_output = inputs
            history[name] = history_output

        for i in range(0, len(self._pipelines)):
            pipefunc = self._pipelines[i]

            args = self._args[i]

            if len(args) == 0:
                outputs = pipefunc(inputs)
            else:
                outputs = pipefunc(inputs, *args)

            if i in self._tags:
                # copy output and put it into history, but only the tagged one
                ## get the tagged name
                name = self._tags[i]
                history_output = copy.copy(outputs)
                history[name] = history_output
            # update inputs
            inputs = outputs

            # merged if needed
            if i in self._merges:
                pipeline = Pipe("merge")
                pipefunc = pipeline.function()
                # update outputs for merge
                outputs = pipefunc(inputs, self._merges[i], history)
                # update inputs agains
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
        # tag the last pipe index
        self._tags[len(self._pipelines) - 1] = name
        return self

    def merge(self, *args):
        # does not make sense to call merge when nothing else to merge
        idx = len(self._pipelines) - 1
        if idx == -1:
            raise ValueError("does not have other things to merge with")
        # store the names in the dict
        self._merges[idx] = list(args)
        return self

    @classmethod
    def add_alias(self, name: str, function) -> None:
        Pipe.add_alias(name, function)
        setattr(self, name, function)
