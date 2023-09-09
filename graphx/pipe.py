from typing import List

from .vertex import Vertex

import copy


class Pipe:
    def __init__(self, operation: str) -> None:
        self._operation = operation

    # decide which function to return based on operation

    def function(self):
        op_map = {
            "forward": self.forward,
            "backward": self.backward,
            "unique": self.unique,
            "take": self.take,
        }

        f = op_map.get(self._operation, None)

        if f is None:
            raise KeyError("program does not support the alias:" + self._operation)
        return f

    def forward(self, args: List[Vertex]) -> List[Vertex]:
        result = []
        for arg in args:
            result += arg.get_to()
        return result

    def backward(self, args: List[Vertex]) -> List[Vertex]:
        result = []
        for arg in args:
            result += arg.get_from()
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
