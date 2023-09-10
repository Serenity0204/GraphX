from typing import List
import copy


def copy_list(objects: List) -> List:
    copies = []
    for obj in objects:
        copied = copy.copy(obj)
        copies.append(copied)
    return copies


def decide_query(kwargs) -> str:
    start = "name_startswith"
    end = "name_endswith"
    contain = "name_contains"
    equal = "name_is"

    query = None
    if start in kwargs:
        query = start
    if end in kwargs:
        query = end
    if contain in kwargs:
        query = contain
    if equal in kwargs:
        query = equal

    return query
