import factory
import factory.fuzzy
from factory.random import randgen
from factory.django import DjangoModelFactory
from .models import StudentCard, Student, ATRCardType, RaspiTag, Board, Semester, StudentGroup, BoardType, BoardStatus


class FuzzyUid(factory.fuzzy.BaseFuzzyAttribute):
    def __init__(self, length):
        self.length = length
        self().__init__()

    def _segment(self):
        x = randgen.randint(0, 255)
        return "{:02X}".format(x)

    def fuzz(self):
        return ' '.join([self._segment() for _ in range(self.length)])


class StudentCardFactory(DjangoModelFactory):
    class Meta:
        model = StudentCard

    atr_hex = ATRCardType.STUDENT_CARD_ATR
    uid = FuzzyUid(length=7)


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    student_card = factory.SubFactory(StudentCardFactory)
    semester = Semester.objects.get_or_create(semester="WS20/21")
    first_name = factory.Faker('first_name')
    second_name = factory.Faker('last_name')
    matricul_no = factory.Faker('random_int', min=850000, max=950000)
    hrz_no = factory.Faker('random_int', min=65000, max=69000)
    group = StudentGroup.A_GROUP
    is_home_loan_enabled = True


class RaspiTagFactory(DjangoModelFactory):
    class Meta:
        model = RaspiTag

    atr_hex = ATRCardType.STUDENT_CARD_ATR
    uid = FuzzyUid(length=4)


class BoardLabFactory(DjangoModelFactory):
    class Meta:
        model = Board

    raspi_tag = factory.SubFactory(RaspiTagFactory)
    board_type = BoardType.LAB_LOAN
    board_status = BoardStatus.ACTIVE


class BoardHomeFactory(DjangoModelFactory):
    class Meta:
        model = Board

    raspi_tag = factory.SubFactory(RaspiTagFactory)
    board_type = BoardType.HOME_LOAN
    board_status = BoardStatus.ACTIVE
