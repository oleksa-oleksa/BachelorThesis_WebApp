from django.db import models
from django.forms import ModelForm
from django_enumfield import enum
from django.core.exceptions import ValidationError
import datetime
from django_fsm import FSMField, transition, RETURN_VALUE, GET_STATE
from django.core.exceptions import ValidationError


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
	START_SESSION = 6
	UNKNOWN_OPERATION = 7


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

	def get_student_boards(self):
		# boards = {"lab": "", "home": ""}
		boards = {}
		lab_board_action = self.action_set.filter(operation=Operation.LAB_LOAN).last()
		home_board_action = self.action_set.filter(operation=Operation.HOME_LOAN).last()

		if lab_board_action is not None:
			if lab_board_action.board.board_status == BoardStatus.LOANED:
				boards["lab"] = lab_board_action.board

		if home_board_action is not None:
			if home_board_action.board.board_status == BoardStatus.LOANED:
				boards["home"] = home_board_action.board

		return boards

	@staticmethod
	def home_loan_enabled(student):
		return student.is_home_loan_enabled


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
	board_no = models.IntegerField('board number', unique=True)
	board_type = enum.EnumField(BoardType, default=BoardType.LAB_LOAN)
	board_status = enum.EnumField(BoardStatus, default=BoardStatus.ACTIVE)
	
	class Meta:
		ordering = ['board_no']
		
	def __str__(self):
		if self.raspi_tag is not None:
			return 'Board ' + str(self.board_no)
		else:
			return 'Board ' + str(self.board_no)

	@staticmethod
	def return_board(raspi_tag):
		# Update the status of the board with raspi_tag
		Board.objects.filter(raspi_tag=raspi_tag).update(board_status=BoardStatus.ACTIVE)

	@staticmethod
	def loan_board(raspi_tag):
		# Update the status of the board with raspi_tag
		Board.objects.filter(raspi_tag=raspi_tag).update(board_status=BoardStatus.LOANED)


class Action(models.Model):
	"""
	Holds the record about the loan operation, student, board and time
	Primary key = default django primary key
	"""
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
	board = models.ForeignKey(Board, on_delete=models.SET_NULL, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now=True)
	operation = enum.EnumField(Operation, default=Operation.UNKNOWN_OPERATION)

	class Meta:
		ordering = ['timestamp']

	@staticmethod
	def return_board_action(student, board, timestamp=datetime.datetime.now, operation=Operation.RETURN_BOARD):
		returned_board_action = Action(student=student, board=board, operation=operation)
		returned_board_action.save()

	@staticmethod
	def loan_board_action(student, board, operation, timestamp=datetime.datetime.now):
		loaned_board_action = Action(student=student, board=board, operation=operation)
		loaned_board_action.save()


class Session(models.Model):
	"""
	Holds the information about the interaction between user (student) and system
	Primary key = default django primary key
	"""

	TERMINAL_STATES = ['timeout', 'finished', 'canceled', 'error_terminated']

	start_time = models.DateTimeField(default=datetime.datetime.now)
	state = FSMField(default='session_started')
	last_action_time = models.DateTimeField(auto_now=True)
	student_card = models.ForeignKey(StudentCard, on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
	raspi_tag = models.ForeignKey(RaspiTag, on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

	class Meta:
		ordering = ['id']

	@staticmethod
	def get_active_session():
		return Session.objects.exclude(state__in=Session.TERMINAL_STATES).last()

	def get_active_board(self):
		if self.raspi_tag is None:
			return None
		return self.raspi_tag.board

	def get_active_student(self):
		if self.student_card is None:
			return None
		return self.student_card.student

	def board_returned(self):
		student = self.get_active_student()
		boards = self.student_card.student.get_student_boards()
		scanned_board = self.get_active_board()

		# return loaned board that is assigned on student- OK
		if scanned_board in boards.values():
			# create action in Action model with returning operation and timestamp
			Action.return_board_action(student=student, board=scanned_board)
			return True
		else:
			return False

	def board_loaned(self):
		scanned_board = self.get_active_board()

		if scanned_board.board_status != BoardStatus.ACTIVE:
			return 'error'

		student = self.get_active_student()
		# if student has 2 boards, they can not loan one more
		boards = student.get_student_boards()
		if len(boards) == 2:
			return 'maximum_boards_reached'
		elif len(boards) == 1:
			if "lab" in boards:
				loaned_type = BoardType.LAB_LOAN
			elif "home" in boards:
				loaned_type = BoardType.HOME_LOAN
			else:
				return 'status_error'
		else:
			loaned_type = 'empty'

		if scanned_board.board_type == loaned_type:
			return 'same_bord_type'

		if scanned_board.board_type == BoardType.LAB_LOAN:
			operation = Operation.LAB_LOAN
		elif scanned_board.board_type == BoardType.HOME_LOAN:
			if not student.is_home_loan_enabled:
				return 'home_loan_disabled'
			operation = Operation.HOME_LOAN

		# create action in Action model with loan operation and timestamp
		Action.loan_board_action(student=student, board=scanned_board, operation=operation)
		return 'loaned'

	def clean(self):
		open_session = Session.objects.exclude(state__in=Session.TERMINAL_STATES).count()
		if open_session != 0:
			raise ValidationError('Active session already exists!')
		super().clean()

	# =================== Django Finite State Machine ===================================

	@transition(field=state, source='session_started', target=RETURN_VALUE('valid_student_card', 'unknown_student_card'))
	def student_card_inserted(self, card_uid):
		try:
			card = StudentCard.objects.get(uid=card_uid)
		except StudentCard.DoesNotExist:
			return 'unknown_student_card'
		try:
			if card.student is not None:
				self.student_card = card
				return 'valid_student_card'
		except StudentCard.student.RelatedObjectDoesNotExist:
			return 'unknown_student_card'

	@transition(field=state, source='valid_student_card', target=RETURN_VALUE('valid_rfid', 'unknown_rfid'))
	def rfid_inserted(self, uid):
		tag = RaspiTag.objects.get(uid=uid)

		try:
			if tag.board is not None:
				self.raspi_tag = tag
				return 'valid_rfid'
		except RaspiTag.board.RelatedObjectDoesNotExist:
			return 'unknown_rfid'

	@transition(field=state, source='valid_rfid',
				target=RETURN_VALUE('rfid_state_loaned', 'rfid_state_active', 'status_error'))
	def get_rfid_status(self):
		board = self.get_active_board()
		if board.board_status == BoardStatus.LOANED:
			return 'rfid_state_loaned'
		elif board.board_status == BoardStatus.ACTIVE:
			return 'rfid_state_active'
		else:
			return 'status_error'

	@transition(field=state, source='rfid_state_loaned', target=RETURN_VALUE('returned', 'return_error'))
	def loaned_board_returned(self):
		if self.board_returned():
			# After the new Action in DB was created with board_returned()
			# # the board_status will be set to Active again
			Board.return_board(self.raspi_tag)
			return 'returned'
		else:
			return 'return_error'

	@transition(field=state, source='rfid_state_active', target=RETURN_VALUE('loaned', 'home_loan_disabled', 'error',
																			 'maximum_boards_reached', 'same_bord_type'))
	def loan_active_board(self):
		result = self.board_loaned()
		if result == 'loaned':
			# After the new Action in DB was created with board_returned()
			# # the board_status will be set to Active again
			Board.loan_board(self.raspi_tag)
		return result

	@transition(field=state, source='*', target='timeout')
	def timeout(self):
		# transition into final state
		pass

	@transition(field=state, source='*', target='canceled')
	def session_canceled(self):
		# transition into final state
		pass

	# SUCCESS FINISH
	@transition(field=state, source=['returned', 'loaned'], target='finished')
	def session_finished(self):
		# finish session, terminal state
		pass

	# ERROR TERMINATION
	@transition(field=state, source=['unknown_student_card', 'unknown_rfid', 'status_error', 'home_loan_disabled',
									'maximum_boards_reached', 'same_bord_type', 'return_error'],
									target='error_terminated')
	def session_terminated(self):
		# change error state to terminated state to allow new session to be started
		pass
