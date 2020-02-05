class Board:
    """
    Represents the Raspberry Pi board at university laboratory
    There are 15 boards and every board has a number and a RFID Tag on it.
    The boards numbered 0-10 should be used in the laboratory during the exercise lesson.
    The boards numbered 11-15 could be loaned by authorised student for home usage.
    """
    def __init__(self, board_uid=None, board_no=0, board_type=None, board_status='Active',
                 is_board_loaned=False, loan_date=None, student=None):
        """Creates a new board with given parameters"""
        self.board_uid = board_uid
        self.board_no = board_no
        self.board_type = board_type
        self.board_status = board_status
        self.is_board_loaned = is_board_loaned
        self.loan_date = loan_date
        self.student = student


