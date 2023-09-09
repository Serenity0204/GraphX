from typing import List
import copy


def copy_list(objects: List) -> List:
    copies = []
    for obj in objects:
        copied = copy.copy(obj)
        copies.append(copied)
    return copies
