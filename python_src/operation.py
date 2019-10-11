from enum import Enum


class Operation(Enum):
    """Represents different operations that could be done by student or admin"""
    labLoan = 1
    homeLoan = 2
    returnBoard = 3
    enableHomeLoan = 4
    disableHomeLoan = 5
    unknownOperation = 6

