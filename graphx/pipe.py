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

    # def filter(self, args: List[Vertex], query_type, attribute) -> List[Vertex]:

    #     # filter only supports _startswith, _contains, _endswith, and _is

    #     result = []
    #     for arg in args:

    #         if not arg.values()
    #     pass

    # check = (

    #     query_type != "name_startswith"

    #     and query_type != "name_contains"

    #     and query_type != "name_endswith"

    #     and query_type != "name_is"

    # )

    # if not check:

    #     raise ValueError(

    #         "filter only supports name_startswith, name_contains, name_endswith, and name_is"

    #     )

    # result = []
    # for arg in args:

    #     if query_type == "name_startswith":
    #         pass

    #     if query_type == "name_contains":
    #         pass

    #     if query_type == "name_endswith":
    #         pass

    #     if query_type == "name_is":
    #         pass

    # return result
