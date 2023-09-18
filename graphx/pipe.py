from typing import List, Dict
from .vertex import Vertex
import copy


class Pipe:
    op_map = {}

    def __init__(self, operation: str) -> None:
        self._operation = operation
        self.setup()

    def setup(self) -> None:
        Pipe.op_map["forward"] = self.forward
        Pipe.op_map["backward"] = self.backward
        Pipe.op_map["unique"] = self.unique
        Pipe.op_map["take"] = self.take
        Pipe.op_map["filter"] = self.filter
        Pipe.op_map["exclude"] = self.exclude
        Pipe.op_map["sort"] = self.sort
        Pipe.op_map["merge"] = self.merge

    def name(self) -> str:
        return self._operation

    # decide which function to return based on operation
    def function(self):
        f = Pipe.op_map.get(self._operation, None)

        if f is None:
            raise KeyError("program does not support the alias:" + self._operation)
        return f

    def forward(self, args: List[Vertex], query=None, name=None) -> List[Vertex]:
        result = []
        for arg in args:
            result += arg.get_to(query, name)
        return result

    def backward(self, args: List[Vertex], query=None, name=None) -> List[Vertex]:
        result = []
        for arg in args:
            result += arg.get_from(query, name)
        return result

    def unique(self, args: List[Vertex]) -> List[Vertex]:
        result = []

        seen = set()
        for arg in args:
            if arg not in seen:
                seen.add(arg)
                result.append(arg)
        return result

    def take(self, args: List[Vertex], num: int) -> List[Vertex]:
        result = []

        count = 0
        for arg in args:
            if count == num:
                break
            result.append(arg)
            count += 1
        return result

    def _filter(self, args: List[Vertex], values, mode) -> List[Vertex]:
        result = []
        for arg in args:
            if arg.values() in values and mode == "filter":
                result.append(arg)
            ## Not correct
            if arg.values() not in values and mode == "exclude":
                result.append(arg)
        return result

    def filter(self, args: List[Vertex], values) -> List[Vertex]:
        return self._filter(args, values, "filter")

    def exclude(self, args: List[Vertex], values) -> List[Vertex]:
        return self._filter(args, values, "exclude")

    ## value has to be sortable
    def sort(self, args: List[Vertex], ascending=True) -> List[Vertex]:
        result = args.copy()
        result.sort(key=lambda x: x.values(), reverse=not ascending)
        return result

    ## merge into pre-existing args helper
    def merge(self, args: List[Vertex], names: List, history: Dict):
        result = args.copy()
        for name in names:
            if name in history:
                result += history[name]
        return result

    # the function should return self
    @classmethod
    def add_alias(self, name: str, function) -> None:
        if name in Pipe.op_map:
            raise ValueError("alias with name=" + name + " already exists")
        if not callable(function):
            raise TypeError("cannot add non function type as alias")
        Pipe.op_map[name] = function
        setattr(self, name, function)
