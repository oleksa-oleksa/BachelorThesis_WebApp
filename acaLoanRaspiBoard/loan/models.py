from django.db import models
from django.forms import ModelForm
from django_enumfield import enum
import datetime


class ATRCardType(enum.Enum):
	"""Constant values for ATR ot student card and RFID tags on the Raspberry Pi"""
	STUDENT_CARD_ATR = 1
	RASPI_TAG_ATR = 2


class StudentCard(models.Model):
	"""
	Student card class
	Primary key = default django primary key
	Each card contains an integrated chip with a permanent identification number, or UID. 
	This number is created during the manufacturing process, it is sometimes referred to as the card serial number.
	
	One unique student card belongs to only one student
	"""
	atr_hex = enum.EnumField(ATRCardType, default=ATRCardType.STUDENT_CARD_ATR)
	uid = models.CharField('Card UID', max_length=66, unique=True)

	def __str__(self):
		return self.uid


class RaspiTag(models.Model):
	"""
	Raspberry board RFID
	Primary key = default django primary key
	One unique rfig tag belongs to one physical Raspberry Board
	"""
	atr_hex = enum.EnumField(ATRCardType, default=ATRCardType.RASPI_TAG_ATR)
	uid = models.CharField('Card UID', max_length=66, unique=True)

	def __str__(self):
		return self.uid


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
	LAB_LOAN = 1
	HOME_LOAN = 2


class BoardStatus(enum.Enum):
	ACTIVE = 1
	LOANED = 2
	OUT_OF_ORDER = 3
	LOST = 4
	UNDEFINED = 5


class Semester(models.Model):
	semester = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.semester


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
	student_card = models.OneToOneField(StudentCard, on_delete=models.SET_NULL, blank=True, null=True)
	semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
	first_name = models.CharField('first name', max_length=50)
	second_name = models.CharField('second name', max_length=50)
	matricul_no = models.CharField('matriculation', max_length=10, unique=True)
	hrz_no = models.CharField('hrz', max_length=10, unique=True)
	group = enum.EnumField(StudentGroup)
	is_home_loan_enabled = models.BooleanField(default=True)
	
	class Meta:
		ordering = ['second_name']

	def __str__(self):
		return self.first_name + ' ' + self.second_name


class Board(models.Model):
	"""
	Class for representation of the Raspberry Pi board at university laboratory
	There are 15 boards and every board has a number and a RFID Tag on it.
	The boards numbered 0-10 should be used in the laboratory during the exercise lesson (BoardLabLoan class)
	The boards numbered 11-15 could be loaned by authorised student for home usage (BoardHomeLoan class)
	Primary key = default django primary key
	Each board has only one unuqie rfid tag
	"""
	raspi_tag = models.OneToOneField(RaspiTag, on_delete=models.SET_NULL, blank=True, null=True)
	board_no = models.CharField('board number', max_length=3, unique=True)
	board_type = enum.EnumField(BoardType, default=BoardType.LAB_LOAN)
	board_status = enum.EnumField(BoardStatus, default=BoardStatus.ACTIVE)
	
	class Meta:
		ordering = ['board_no']
		
	def __str__(self):
		if self.raspi_tag is not None:
			return 'Board ' + self.board_no
		else:
			return 'Board ' + self.board_no


class Action(models.Model):
	"""
	Holds the record about the loan operation, student, board and time      
	Primary key = default django primary key
	"""
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	timestamp = models.DateField(default=datetime.date.today)
	operation = enum.EnumField(Operation, default=Operation.UNKNOWN_OPERATION)

	class Meta:
		ordering = ['timestamp']