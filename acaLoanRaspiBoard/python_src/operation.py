from enum import Enum


class Operation(Enum):
    """Represents different operations that could be done by student or admin"""
    lab_loan = 1
    home_loan = 2
    return_board = 3
    enable_home_loan = 4
    disable_home_loan = 5
    unknown_operation = 6

