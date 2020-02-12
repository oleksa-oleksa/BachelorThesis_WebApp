from django.db import models
from python_src import board_type, board_status


class Student(models.Model):
	studentcard_uid = models.CharField(max_length=50, primary_key=True)
	first_name = models.CharField('first name', max_length=50)
	second_name = models.CharField('second name', max_length=50)
	matricul_no = models.CharField('matriculation', max_length=10, unique=True)
	hrz_no = models.CharField('hrz', max_length=10, unique=True)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	is_home_loan_enabled = models.BooleanField(default=True)
	list_of_board = list_of_boards
 

class Board(models.Model):
	board_uid = models.CharField(max_length=50, primary_key=True)
	board_no = models.CharField('board number', max_length=10, unique=True)
	board_type = models.CharField(max_length=10, types=[(t_board, t_board.value) for t_board in BoardType]  # types is a list of Tuple
	board_status = models.CharField(max_length=10, states=[(t_status, t_status.value) for t_status in BoardStatus]  # types is a list of Tuple
	is_board_loaned = models.BooleanField(default=False)
	loan_date = loan_date
	student = student

