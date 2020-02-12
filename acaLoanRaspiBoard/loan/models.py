from django.db import models 
from django_enumfield import enum
from python_src import board_type, board_status


class StudentCard(models.Model):
	atr_hex = models.CharField('ATR HEX', max_length=66)
	uid = models.CharField('Card UID', max_length=66, unique=True)


class RaspiTag(models.Model):
	atr_hex = models.CharField('ATR HEX', max_length=66)
	uid = models.CharField('Card UID', max_length=66, unique=True)
		

class StudentGroup(enum.Enum):
	A_GROUP = 1
	B_GROUP = 2
	

class Operation(enum.Enum):
	"""Represents different operations that could be done by student or admin"""
	LAB_LOAN = 1
	HOME_LOAN = 2
	RETURN_BOARD = 3
	ENABLE_HOME_LOAN = 4
	DISABLE_HOME_LOAN = 5
	UNKNOWN_OPERATION = 6


class BoardType(enum.Enum):
    """Represents two types of boards: for laboratory usage only and for home loan only"""
    LAB_LOAN = 1
    HOME_LOAN = 2


class Student(models.Model):
	 """
    Represents a student in database. The personal date will be specified
    by the admin after student has made enrollment to the course.
    The group will be specified on the first lecture by the students/teaching assistance
    home_loan_enabled flag is to set by the admin in case the board was returned damaged
    and a student has not notified the teaching assistance about what happened
    """
	studentcard = models.OneToOneField(
        StudentCard,
        on_delete=models.CASCADE,
        primary_key=True,
    )
	first_name = models.CharField('first name', max_length=50)
	second_name = models.CharField('second name', max_length=50)
	matricul_no = models.CharField('matriculation', max_length=10, unique=True)
	hrz_no = models.CharField('hrz', max_length=10, unique=True)
	group = enum.EnumField(StudentGroup)
	is_home_loan_enabled = models.BooleanField(default=True)
 


class Board(models.Model):
	raspi_tag = models.OneToOneField(
        RaspiTag,
        on_delete=models.CASCADE,
        primary_key=True,
    )
	board_no = models.CharField('board number', max_length=10, unique=True)
	board_type = models.CharField(max_length=10, types=[(t_board, t_board.value) for t_board in BoardType]  # types is a list of Tuple
	board_status = models.CharField(max_length=10, states=[(t_status, t_status.value) for t_status in BoardStatus]  # types is a list of Tuple
	is_board_loaned = models.BooleanField(default=False)
	loan_date = models.DateField()


class LogEntry(models.Model):
    """
    Holds the record about the loan operation, student, board and time
    """
    def __init__(self, student=None, board=None, timestamp=None, operation=6):
        """A single entry about board loan/return operation"""
        self.student = student
        self.board = board
        self.timestamp = timestamp
        self.operation = Operation(operation)

	
