class Board:
    """
    Represents the Raspberry Pi board at university laboratory
    There are 15 boards and every board has a number and a RFID Tag on it.
    The boards numbered 0-10 should be used in the laboratory during the exercise lesson.
    The boards numbered 11-15 could be loaned by authorised student for home usage.
    """
    def __init__(self, board_no=0, board_rfid_tag=None, loan_type=None):
        """Creates a new board with given parameters"""


