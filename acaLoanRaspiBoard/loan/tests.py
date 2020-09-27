from django.test import TestCase
from .models import StudentCard, Student, RaspiTag, Board, ATRCardType, Semester, StudentGroup, BoardType, BoardStatus, Session
from . import factories


# Create your tests here.
class TestHomeLoanBoard(TestCase):
    def setUp(self):
        semester = Semester.objects.create(semester="WS20/21")
        self.student_home_enabled = factories.StudentFactory(semester=semester)
        self.student_home_disabled = factories.StudentFactory(semester=semester, is_home_loan_enabled=False)
        self.lab_board_active = factories.BoardLabFactory(board_no=3)
        self.lab_board_loaned = factories.BoardLabFactory(board_no=4, board_status=BoardStatus.LOANED)
        self.home_board_active = factories.BoardHomeFactory(board_no=13)
        self.home_board_loaned = factories.BoardHomeFactory(board_no=14, board_status=BoardStatus.LOANED)

    def test_home_loan_enabled(self):
        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.home_board_active.raspi_tag)
        self.assertEqual(session.board_loaned(), 'loaned')

    def test_home_loan_disabled(self):
        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_disabled.student_card,
                                         raspi_tag=self.home_board_active.raspi_tag)
        self.assertEqual(session.board_loaned(), 'home_loan_disabled')

