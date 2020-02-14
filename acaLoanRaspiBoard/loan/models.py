from django.db import models 
from django_enumfield import enum
import datetime


class StudentCard(models.Model):
	"""
	Student card class
	Primary key = default django primary key
	Each card contains an integrated chip with a permanent identification number, or UID. 
	This number is created during the manufacturing process, it is sometimes referred to as the card serial number.
	
	One unique student card belongs to only one student
	"""
	atr_hex = models.CharField('ATR HEX', max_length=66)
	uid = models.CharField('Card UID', max_length=66, unique=True)


class RaspiTag(models.Model):
	"""
	Raspberry board RFID
	Primary key = default django primary key
	One unique rfig tag belongs to one physical Raspberry Board
	"""
	atr_hex = models.CharField('ATR HEX', max_length=66)
	uid = models.CharField('Card UID', max_length=66, unique=True)
		

class StudentGroup(enum.Enum):
	A_GROUP = 1
	B_GROUP = 2
	

class Operation(enum.Enum):
	"""Represents different operations that could be done by student or admin on loan system"""
	LAB_LOAN = 1
	HOME_LOAN = 2
	RETURN_BOARD = 3
	ENABLE_HOME_LOAN = 4
	DISABLE_HOME_LOAN = 5
	UNKNOWN_OPERATION = 6


class BoardType(enum.Enum):
	"""Represents two types of boards: for laboratory usage only and for home loan only"""
	LAB_LOAN_BOARD = 1
	HOME_LOAN_BOARD = 2


class BoardStatus(enum.Enum):
	ACTIVE = 1
	LOANED = 2
	OUT_OF_ORDER = 3
	LOST = 4
	UNDEFINED = 5


class Student(models.Model):
	"""
	Represents a student in database. The personal date will be specified
	by the admin after student has made enrollment to the course.
	The group will be specified on the first lecture by the students/teaching assistance
	home_loan_enabled flag is to set by the admin in case the board was returned damaged
	and a student has not notified the teaching assistance about what happened

	Primary key = default django primary key
	Each student has only one unuqie student card
	"""
	studentcard = models.OneToOneField(StudentCard, on_delete=models.CASCADE, primary_key=True,)
	first_name = models.CharField('first name', max_length=50)
	second_name = models.CharField('second name', max_length=50)
	matricul_no = models.CharField('matriculation', max_length=10, unique=True)
	hrz_no = models.CharField('hrz', max_length=10, unique=True)
	group = enum.EnumField(StudentGroup)
	is_home_loan_enabled = models.BooleanField(default=True)
	lab_board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Board(models.Model):
	"""
	Abstract class for the basic representation of the Raspberry Pi board at university laboratory
	There are 15 boards and every board has a number and a RFID Tag on it.
	The boards numbered 0-10 should be used in the laboratory during the exercise lesson (BoardLabLoan class)
	The boards numbered 11-15 could be loaned by authorised student for home usage (BoardHomeLoan class)
	Primary key = default django primary key
	Each board has only one unuqie rfid tag
	"""
	raspi_tag = models.OneToOneField(RaspiTag, on_delete=models.CASCADE, primary_key=True)
	board_no = models.CharField('board number', max_length=10, unique=True)
	board_type = enum.EnumField(BoardType)
	board_status = enum.EnumField(BoardStatus, default=BoardStatus.ACTIVE)
	is_board_loaned = models.BooleanField(default=False)
	
	class Meta:
		abstract = True
		ordering = ['board_no']
		
	def __str__(self):
		return self.board_no + ': ' + self.raspi_tag + 'is loaned: ' + self.is_board_loaned


class BoardLabLoan(Board):
	last_lab_date = models.DateTimeField('date of lab loan/return', blank=True, null=True)
	last_lab_student = models.ForeignKey('student', Student, on_delete=models.CASCADE)
	last_lab_operation = enum.EnumField('type of operation', Operation, default=Operation.UNKNOWN_OPERATION)


class BoardHomeLoan(Board):
	last_home_date = models.DateTimeField('date of home loan/return', blank=True, null=True)
	last_home_student = models.ForeignKey('student', Student, on_delete=models.CASCADE)
	last_home_operation = enum.EnumField('type of operation', Operation, default=Operation.UNKNOWN_OPERATION)

class LogEntry(models.Model):
	"""
	Holds the record about the loan operation, student, board and time      
	Primary key = default django primary key
	Join table
	"""
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	timestamp = models.DateField(default=datetime.date.today)
	operation = enum.EnumField(Operation, default=Operation.UNKNOWN_OPERATION)

