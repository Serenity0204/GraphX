def generate_test_num():
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


def generate_test_person(num):
    vals = []

    for i in range(0, num + 1):
        vals.append(Person(str(i), i))

    return vals


nodes = [1, 2, 3, 4, 5, 6]

edges = [
    {"from": 1, "to": 2, "forward": "son"},
    {"from": 2, "to": 3, "forward": "son"},
    {"from": 2, "to": 4, "forward": "son"},
    {"from": 2, "to": 5, "forward": "son"},
    {"from": 2, "to": 6, "forward": "daughter"},
    {"from": 3, "to": 4, "forward": "brother", "backward": "brother"},
    {"from": 4, "to": 5, "forward": "brother", "backward": "brother"},
    {"from": 5, "to": 3, "forward": "brother", "backward": "brother"},
    {"from": 3, "to": 6, "forward": "sister", "backward": "brother"},
    {"from": 4, "to": 6, "forward": "sister", "backward": "brother"},
    {"from": 5, "to": 6, "forward": "sister", "backward": "brother"},
]
