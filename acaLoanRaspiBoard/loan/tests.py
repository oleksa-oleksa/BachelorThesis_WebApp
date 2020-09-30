from django.test import TestCase
from .models import StudentCard, Student, RaspiTag, Board, ATRCardType, Semester, StudentGroup, BoardType, BoardStatus
from .models import Session, Action, Operation
from . import factories


# Create your tests here.
class TestFSMTransitions(TestCase):
    def setUp(self):
        semester = Semester.objects.create(semester="WS20/21")
        self.student_home_enabled = factories.StudentFactory(semester=semester)
        self.student_home_enabled_second = factories.StudentFactory(semester=semester)
        self.student_home_disabled = factories.StudentFactory(semester=semester, is_home_loan_enabled=False)
        self.lab_board_active = factories.BoardLabFactory(board_no=3)
        self.lab_board_loaned = factories.BoardLabFactory(board_no=4, board_status=BoardStatus.LOANED)
        self.home_board_active = factories.BoardHomeFactory(board_no=13)
        self.home_board_loaned = factories.BoardHomeFactory(board_no=14, board_status=BoardStatus.LOANED)

    def test_valid_student_card_inserted(self):
        session = Session.objects.create(state='session_started', student_card=None,
                                         raspi_tag=None)
        session.student_card_inserted(self.student_home_enabled.student_card.uid)
        self.assertEqual(session.state, 'valid_student_card')

    def test_unknown_student_card_inserted(self):
        rand_student = factories.StudentCardFactory()
        session = Session.objects.create(state='session_started', student_card=None,
                                         raspi_tag=None)
        session.student_card_inserted(rand_student.uid)
        self.assertEqual(session.state, 'unknown_student_card')

    def test_empty_student_card_inserted(self):
        session = Session.objects.create(state='session_started', student_card=None,
                                         raspi_tag=None)
        session.student_card_inserted(None)
        self.assertEqual(session.state, 'unknown_student_card')

    def test_valid_rfid_inserted(self):
        session = Session.objects.create(state='valid_student_card', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        session.rfid_inserted(self.lab_board_active.raspi_tag.uid)
        self.assertEqual(session.state, 'valid_rfid')

    def test_unknown_rfid_inserted(self):
        rand_rfid = factories.RaspiTagFactory()
        session = Session.objects.create(state='valid_student_card', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        session.rfid_inserted(rand_rfid.uid)
        self.assertEqual(session.state, 'unknown_rfid')

    def test_empty_rfid_inserted(self):
        session = Session.objects.create(state='valid_student_card', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        session.rfid_inserted(None)
        self.assertEqual(session.state, 'unknown_rfid')

    def test_get_rfid_status_loaned(self):
        session = Session.objects.create(state='valid_rfid', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_loaned.raspi_tag)
        session.get_rfid_status()
        self.assertEqual(session.state, 'rfid_state_loaned')

    def test_get_rfid_status_active(self):
        session = Session.objects.create(state='valid_rfid', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_active.raspi_tag)
        session.get_rfid_status()
        self.assertEqual(session.state, 'rfid_state_active')

    def test_get_rfid_status_none(self):
        session = Session.objects.create(state='valid_rfid', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        session.get_rfid_status()
        self.assertEqual(session.state, 'status_error')




class TestLabLoanBard(TestCase):
    def setUp(self):
        semester = Semester.objects.create(semester="WS20/21")
        self.student_home_enabled = factories.StudentFactory(semester=semester)
        self.student_home_enabled_second = factories.StudentFactory(semester=semester)
        self.student_home_disabled = factories.StudentFactory(semester=semester, is_home_loan_enabled=False)
        self.lab_board_active = factories.BoardLabFactory(board_no=3)
        self.lab_board_loaned = factories.BoardLabFactory(board_no=4, board_status=BoardStatus.LOANED)
        self.home_board_active = factories.BoardHomeFactory(board_no=13)
        self.home_board_loaned = factories.BoardHomeFactory(board_no=14, board_status=BoardStatus.LOANED)

    def test_lab_loan(self):
        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_active.raspi_tag)
        self.assertEqual(session.board_loaned(), 'loaned')

    def test_lab_return(self):
        session = Session.objects.create(state='rfid_state_loaned', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_loaned.raspi_tag)
        # link student and and board
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)
        self.assertEqual(session.loaned_board_returned(), 'returned')

    def test_loan_second_board_same_type(self):
        # loan first board
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_active.raspi_tag)
        self.assertEqual(session.board_loaned(), 'same_bord_type')

    def test_loan_same_board_twice(self):
        # loan first time
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_loaned.raspi_tag)
        # board_status != BoardStatus.ACTIVE
        self.assertEqual(session.board_loaned(), 'error')

        # change board status to be active again but no record about return operation is exist
        self.lab_board_loaned.board_status = BoardStatus.ACTIVE
        self.assertEqual(session.board_loaned(), 'same_bord_type')

    def test_home_return_unassigned_board(self):
        # loan board to a first student
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        # create a session for a second student and scan a previous loaned board
        session = Session.objects.create(state='rfid_state_loaned', student_card=self.student_home_enabled_second.student_card,
                                         raspi_tag=self.lab_board_loaned.raspi_tag)

        self.assertEqual(session.loaned_board_returned(), 'return_error')

    def test_home_loan_third_board(self):
        # create record about first loan
        Action.loan_board_action(student=self.student_home_enabled, board=self.home_board_loaned,
                                 operation=Operation.HOME_LOAN)
        # create record about second loan
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        # scan student card and third active board
        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_active.raspi_tag)

        # try to loan
        self.assertEqual(session.board_loaned(), 'maximum_boards_reached')


class TestHomeLoanBoard(TestCase):
    def setUp(self):
        semester = Semester.objects.create(semester="WS20/21")
        self.student_home_enabled = factories.StudentFactory(semester=semester)
        self.student_home_enabled_second = factories.StudentFactory(semester=semester)
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

    def test_home_return(self):
        session = Session.objects.create(state='rfid_state_loaned', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.home_board_loaned.raspi_tag)
        # link student and and board
        Action.loan_board_action(student=self.student_home_enabled, board=self.home_board_loaned,
                                 operation=Operation.HOME_LOAN)
        self.assertEqual(session.loaned_board_returned(), 'returned')

    def test_loan_second_board_same_type(self):
        # loan first board
        Action.loan_board_action(student=self.student_home_enabled, board=self.home_board_loaned,
                                 operation=Operation.HOME_LOAN)

        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.home_board_active.raspi_tag)
        self.assertEqual(session.board_loaned(), 'same_bord_type')

    def test_loan_same_board_twice(self):
        # loan first time
        Action.loan_board_action(student=self.student_home_enabled, board=self.home_board_loaned,
                                 operation=Operation.HOME_LOAN)

        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.home_board_loaned.raspi_tag)
        # board_status != BoardStatus.ACTIVE
        self.assertEqual(session.board_loaned(), 'error')

        # change board status to be active again but no record about return operation is exist
        self.home_board_loaned.board_status = BoardStatus.ACTIVE
        self.assertEqual(session.board_loaned(), 'same_bord_type')

    def test_home_return_unassigned_board(self):
        # loan board to a first student
        Action.loan_board_action(student=self.student_home_enabled, board=self.home_board_loaned,
                                 operation=Operation.HOME_LOAN)

        # create a session for a second student and scan a previous loaned board
        session = Session.objects.create(state='rfid_state_loaned', student_card=self.student_home_enabled_second.student_card,
                                         raspi_tag=self.home_board_loaned.raspi_tag)

        self.assertEqual(session.loaned_board_returned(), 'return_error')

    def test_home_loan_third_board(self):
        # create record about first loan
        Action.loan_board_action(student=self.student_home_enabled, board=self.home_board_loaned,
                                 operation=Operation.HOME_LOAN)
        # create record about second loan
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        # scan student card and third active board
        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.home_board_active.raspi_tag)

        # try to loan
        self.assertEqual(session.board_loaned(), 'maximum_boards_reached')

    def test_home_loan_non_existing_board(self):
        rand_rfid = factories.RaspiTagFactory()
        session = Session.objects.create(state='rfid_state_active', student_card=self.student_home_enabled.student_card,
                                         raspi_tag=rand_rfid)
        with self.assertRaises(RaspiTag.board.RelatedObjectDoesNotExist):
            session.board_loaned()


