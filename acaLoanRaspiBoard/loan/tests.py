from django.test import TestCase
from .models import StudentCard, Student, RaspiTag, Board, ATRCardType, Semester, StudentGroup, BoardType, BoardStatus, Session
from . import factories


# Create your tests here.
class TestHomeLoanBoard(TestCase):
    def setUp(self):
        self.student_home_enabled = factories.StudentFactory()
        self.student_home_disabled = factories.StudentFactory(is_home_loan_enabled=False)
        self.lab_board_active = factories.BoardLabFactory()
        self.lab_board_loaned = factories.BoardLabFactory(board_status=BoardStatus.LOANED)
        self.home_board_active = factories.BoardHomeFactory()
        self.home_board_loaned = factories.BoardHomeFactory(board_status=BoardStatus.LOANED)

    def test_home_loan_enabled(self):
        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card, raspi_tag=self.home_board_active)
        self.assertEqual(session.board_loaned(), 'loaned')