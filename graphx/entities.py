import uuid
import copy
from typing import Dict, List


# Vertex class that the edge instance will connect 2 of its instance
class Vertex:
    def __init__(self, value) -> None:
        self._from = []
        self._to = []
        # deep copy the value to prevent original data being modified
        self._value = copy.deepcopy(value)
        self._id = uuid.uuid4()

    def value(self):
        return self._value

    def id(self):
        return self._id

    def get_from(self) -> List:
        return self._from

    def get_to(self) -> List:
        return self._to

    def add_from(self, v) -> None:
        self._from.append(v)

    def add_to(self, v) -> None:
        self._to.append(v)

    def __str__(self) -> str:
        return str(self._value)

    ## for comparing
    def __eq__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self._recursive_eq(self._value, other._value)
        return False

    def _recursive_eq(self, obj1, obj2) -> bool:
        if hasattr(obj1, "__dict__") and hasattr(obj2, "__dict__"):
            return obj1.__dict__ == obj2.__dict__
        return obj1 == obj2


# Edge class for graph
class Edge:
    def __init__(
        self,
        src: Vertex,
        dest: Vertex,
        forward_name="forward",
        backward_name="backward",
        has_backward=False,
    ) -> None:
        # record both directions if needed
        self._has_backward = has_backward

        # forward
        self._forward_from = src
        self._forward_to = dest
        self._forward_name_as = forward_name

        # backward
        if has_backward:
            self._backward_from = dest
            self._backward_to = src
            self._backward_name_as = backward_name

        # add from and to for the input src and dest
        # example
        """
        Person p1, p2
        p1 -> p2 as brother
        p2 -> p1 as sister
        means p2 is p1's brother
        and p1 is p2's sister if has_backward = true
        """

    def get_forward_info(self) -> Dict:
        info = {
            "from": self._forward_from,
            "to": self._forward_to,
            "name": self._forward_name_as,
        }
        return info

    def get_backward_info(self) -> Dict:
        # if not backward then return empty dict
        if not self._has_backward:
            return {}
        info = {
            "from": self._backward_from,
            "to": self._backward_to,
            "name": self._backward_name_as,
        }
        return info
