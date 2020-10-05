from django.test import TestCase
from ..models import StudentCard, Student, RaspiTag, Board, ATRCardType, Semester, StudentGroup, BoardType, BoardStatus
from ..models import Session, Action, Operation
from . import factories
from django.urls import reverse
from django.test import Client


class TestAPI(TestCase):
    def setUp(self):
        semester = Semester.objects.create(semester="WS20/21")
        self.student_home_enabled = factories.StudentFactory(semester=semester)
        self.student_home_enabled_second = factories.StudentFactory(semester=semester)
        self.student_home_disabled = factories.StudentFactory(semester=semester, is_home_loan_enabled=False)
        self.lab_board_active = factories.BoardLabFactory(board_no=3)
        self.lab_board_loaned = factories.BoardLabFactory(board_no=4, board_status=BoardStatus.LOANED)
        self.home_board_active = factories.BoardHomeFactory(board_no=13)
        self.home_board_loaned = factories.BoardHomeFactory(board_no=14, board_status=BoardStatus.LOANED)
        self.csrf_client = Client(enforce_csrf_checks=True)

    def test_session_started(self):
        response = self.csrf_client.post(reverse('sessions_list'))
        self.assertEqual(response.status_code, 201)

    def test_session_started_twice(self):
        response_ok = self.csrf_client.post(reverse('sessions_list'))
        self.assertEqual(response_ok.status_code, 201)

        response_bad = self.csrf_client.post(reverse('sessions_list'))
        self.assertEqual(response_bad.status_code, 403)

    def test_session_started_active_existed(self):
        Session.objects.create(state='valid_rfid', student_card=self.student_home_enabled.student_card,
                               raspi_tag=self.lab_board_loaned.raspi_tag)
        response_bad = self.csrf_client.post(reverse('sessions_list'))
        self.assertEqual(response_bad.status_code, 403)

    def test_session_started_after_termination(self):
        Session.objects.create(state='finished', student_card=self.student_home_disabled.student_card,
                               raspi_tag=self.home_board_loaned.raspi_tag)

        response = self.csrf_client.post(reverse('sessions_list'))
        self.assertEqual(response.status_code, 201)

    def test_valid_student_card_inserted(self):
        session = Session.objects.create(state='session_started', student_card=None, raspi_tag=None)
        payload = {"type": "card", "uid": self.student_home_enabled.student_card.uid}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'valid_student_card')

    def test_unknown_student_card_inserted(self):
        rand_student = factories.StudentCardFactory()
        session = Session.objects.create(state='session_started', student_card=None, raspi_tag=None)
        payload = {"type": "card", "uid": rand_student.uid}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'unknown_student_card')

    def test_empty_student_card_inserted(self):
        session = Session.objects.create(state='session_started', student_card=None, raspi_tag=None)
        payload = {"type": "card", "uid": ""}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'unknown_student_card')

    def test_valid_rfid_inserted(self):
        session = Session.objects.create(state='valid_student_card', student_card=self.student_home_enabled.student_card, raspi_tag=None)
        payload = {"type": "tag", "uid": self.lab_board_active.raspi_tag.uid}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'valid_rfid')

    def test_unknown_rfid_inserted(self):
        rand_rfid = factories.RaspiTagFactory()
        session = Session.objects.create(state='valid_student_card',
                                         student_card=self.student_home_enabled.student_card, raspi_tag=None)
        payload = {"type": "tag", "uid": rand_rfid.uid}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'unknown_rfid')

    def test_empty_rfid_inserted(self):
        session = Session.objects.create(state='valid_student_card',
                                         student_card=self.student_home_enabled.student_card, raspi_tag=None)
        payload = {"type": "tag", "uid": ""}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'unknown_rfid')

    def test_get_rfid_status_loaned(self):
        session = Session.objects.create(state='valid_rfid',
                                         student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_loaned.raspi_tag)
        payload = {"type": "get_rfid_status"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'rfid_state_loaned')

    def test_get_rfid_status_active(self):
        session = Session.objects.create(state='valid_rfid',
                                         student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_active.raspi_tag)
        payload = {"type": "get_rfid_status"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'rfid_state_active')

    def test_get_rfid_status_none(self):
        session = Session.objects.create(state='valid_rfid',
                                         student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        payload = {"type": "get_rfid_status"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'status_error')

    def test_loaned_board_returned(self):
        session = Session.objects.create(state='rfid_state_loaned',
                                         student_card=self.student_home_enabled.student_card,
                                         raspi_tag=self.lab_board_loaned.raspi_tag)
        # link student and and board
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        payload = {"type": "return_scanned_board_button"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'returned')

    def test_loaned_board_returned_no_student(self):
        session = Session.objects.create(state='rfid_state_loaned',
                                         student_card=None,
                                         raspi_tag=self.lab_board_loaned.raspi_tag)

        payload = {"type": "return_scanned_board_button"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'return_error')

    def test_loaned_board_returned_no_board(self):
        session = Session.objects.create(state='rfid_state_loaned',
                                         student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        # link student and and board
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        payload = {"type": "return_scanned_board_button"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'return_error')

    def test_loaned_board_returned_no_board_no_record(self):
        session = Session.objects.create(state='rfid_state_loaned',
                                         student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        payload = {"type": "return_scanned_board_button"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'return_error')

    def test_unassigned_board_returned(self):
        session = Session.objects.create(state='rfid_state_loaned',
                                         student_card=self.student_home_enabled.student_card,
                                         raspi_tag=None)
        # link student and and board
        Action.loan_board_action(student=self.student_home_enabled, board=self.lab_board_loaned,
                                 operation=Operation.LAB_LOAN)

        payload = {"type": "return_scanned_board_button"}
        response = self.csrf_client.post(reverse('events'),
                                         content_type="application/json",
                                         data=payload)
        self.assertEqual(response.status_code, 201)
        session.refresh_from_db()
        self.assertEqual(session.state, 'return_error')

    def test_unlinked_active_board_returned(self):
        pass

    def test_linked_active_board_returned(self):
        pass



