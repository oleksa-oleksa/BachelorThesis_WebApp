from django.test import TestCase
from .models import StudentCard, Student, RaspiTag, Board, ATRCardType, Semester, StudentGroup, BoardType, BoardStatus


# Create your tests here.
class TestHomeLoanBoard(TestCase):
    def setUp(self):
        semester = Semester.objects.create(semester="WS20/21")
        card = StudentCard.objects.create(uid="04 3B 5E CA 9D 56 80")
        student_home_enabled = Student.objects.create(student_card=card, semester=semester, first_name="Alexandra",
                                                    second_name="Baga", matricul_no="849852", hrz_no="s65556",
                                                     group=StudentGroup.A_GROUP, is_home_loan_enabled=True)
        student_home_disabled= Student.objects.create(student_card=card, semester=semester, first_name="Alexandra",
                                                     second_name="Baga", matricul_no="849852", hrz_no="s65556",
                                                     group=StudentGroup.A_GROUP, is_home_loan_enabled=False)
        raspi_tag = RaspiTag.objects.create(uid="EC B8 89 30")
        raspi_tag = RaspiTag.objects.create(uid="EC B8 89 30")
        board_active = Board.objects.create(raspi_tag=raspi_tag, board_no=14, board_type=BoardType.HOME_LOAN,
                                            board_status=BoardStatus.ACTIVE)


    def test_home_loan(self):

        self.assertEqual(student.student_card, card)
        self.assertEqual(board.raspi_tag, raspi_tag)