import copy
from typing import Dict, List
from .utils import copy_list


# Vertex class that the edge instance will connect 2 of its instance
class Vertex:
    def __init__(self, value) -> None:
        # verticies
        # key is vertex, value is name
        self._from = {}
        self._to = {}

        # deep copy the value to prevent original data being modified
        self._value = copy.deepcopy(value)

    def values(self):
        return self._value

    def _filter(self, query, name, mode) -> List:
        result = []
        items = self._from.items() if mode == "from" else self._to.items()
        for key, val in items:
            if query == "name_startswith" and val.startswith(name):
                result.append(key)
            if query == "name_endswith" and val.endswith(name):
                result.append(key)
            if query == "name_contains" and val.find(name) != -1:
                result.append(key)
            if query == "name_is" and val == name:
                result.append(key)
        return copy_list(result)

    def get_from(self, query=None, name=None) -> List:
        if query is None:
            return copy_list(list(self._from.keys()))
        return self._filter(query, name, "from")

    def get_to(self, query=None, name=None) -> List:
        if query is None:
            return copy_list(list(self._to.keys()))
        return self._filter(query, name, "to")

    def add_from(self, v, name) -> None:
        self._from[v] = name

    def add_to(self, v, name) -> None:
        self._to[v] = name

    def __str__(self) -> str:
        return str(self._value)

    def __lt__(self, other):
        return self.values() < other.values()

    def __eq__(self, other):
        return self.values() == other.values()

    ## for comparing
    def __eq__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self._recursive_eq(self._value, other._value)
        return False

    def _recursive_eq(self, obj1, obj2) -> bool:
        if hasattr(obj1, "__dict__") and hasattr(obj2, "__dict__"):
            return obj1.__dict__ == obj2.__dict__
        return obj1 == obj2

    def contains(self, vertex, direction: str, name: str) -> bool:
        if direction != "to" and direction != "from":
            return False

        relationship_name = None
        # search in _to
        if direction == "to":
            # not in to direction
            relationship_name = self._to.get(vertex, None)
            if relationship_name is None:
                return False

        # search in _from
        if direction == "from":
            relationship_name = self._from.get(vertex, None)
            # not in from direction
            if relationship_name is None:
                return False

        # if it's in correct direction, check the name
        # if the name is successfully retrieved
        # check if name equals
        if relationship_name != name:
            return False

        # finally equal
        return True

    # Create a hash based on the dictionary representation of _value
    def __hash__(self):
        if isinstance(self._value, (int, float, str)):
            return hash(self._value)
        if hasattr(self._value, "__dict__"):
            return hash(tuple(sorted(self._value.__dict__.items())))
        else:
            # Handle other cases as needed
            raise TypeError("unsupported type for value")
