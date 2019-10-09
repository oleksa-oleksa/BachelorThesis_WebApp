from enum import Enum


class BoardType(Enum):
    """Represents two types of boards: for laboratory usage only and for home loan only"""
    labLoan = 1
    homeLoan = 2
