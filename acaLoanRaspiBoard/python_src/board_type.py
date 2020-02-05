from enum import Enum


class BoardType(Enum):
    """Represents two types of boards: for laboratory usage only and for home loan only"""
    lab_loan = 1
    home_loan = 2
