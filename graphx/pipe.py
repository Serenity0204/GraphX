from typing import List
from .vertex import Vertex
import copy


class Pipe:
    def __init__(self, operation: str) -> None:
        self._operation = operation
        self._op_map = {}

    # decide which function to return based on operation

    def function(self):
        self._op_map["forward"] = self.forward
        self._op_map["backward"] = self.backward
        self._op_map["unique"] = self.unique
        self._op_map["take"] = self.take

        f = self._op_map.get(self._operation, None)

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

    def _filter(self, args: List[Vertex], value, mode) -> List[Vertex]:
        result = []
        for arg in args:
            if type(arg.values()) != type(value):
                raise TypeError("type is not comparable")
            if value == arg.values() and mode == "filter":
                result.append(arg)
            if value != arg.values() and mode == "exclude":
                result.append(arg)
        return result

    def filter(self, args: List[Vertex], value) -> List[Vertex]:
        return self._filter(args, value, "filter")

    def exclude(self, args: List[Vertex], value) -> List[Vertex]:
        return self._filter(args, value, "exclude")

    ## value has to be sortable
    def sort(self, args: List[Vertex], ascending=True) -> List[Vertex]:
        pass
