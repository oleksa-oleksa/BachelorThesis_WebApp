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
        session = Session.objects.create(state='returned', student_card=self.student_home_disabled.student_card,
                                         raspi_tag=self.home_board_loaned.raspi_tag)
        session.session_finished()
        self.assertEqual(session.state, 'finished')

        response = self.csrf_client.post(reverse('sessions_list'))
        self.assertEqual(response.status_code, 201)

    def test_valid_student_card_inserted(self):
        session = Session.objects.create(state='session_started', student_card=None, raspi_tag=None)
        payload = {"type": "card", "uid": self.student_home_enabled.student_card}
        response = self.csrf_client.post(reverse('events'), json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(session.state, 'valid_student_card')

