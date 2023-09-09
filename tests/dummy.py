import sys

sys.path.append("../")
from graphx import Vertex, GraphX


def generate_test_entities_num():
    vals = [3, 5, 6, 9, 8]
    return vals


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return str("person:" + self.name)

    ## for comparing
    def __eq__(self, other) -> bool:
        if isinstance(other, Person):
            return (self.name == other.name) and (self.age == other.age)
        return False


def generate_test_entities_person():
    vals = []
    for i in range(0, 5):
        vals.append(Person(str(i), i))
    return vals
