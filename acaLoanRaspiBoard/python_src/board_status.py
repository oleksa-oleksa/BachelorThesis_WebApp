from enum import Enum


class BoardStatus(Enum):
    """Represents two types of boards: for laboratory usage only and for home loan only"""
    active = 1
    loaned = 2
    out_of_order = 3
    undefined = 4
