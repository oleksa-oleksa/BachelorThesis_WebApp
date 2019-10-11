from datetime import datetime
from .operation import Operation

class LogEntry:
    """
    Holds the record about the loan operation, student, board and time
    """
    def __init__(self, student=None, board=None, timestamp=None, operation=6):
        """A single entry about board loan/return operation"""
        self.student = student
        self.board = board
        self.timestamp = timestamp
        self.operation = Operation(operation)

