import factory
import factory.fuzzy
from factory.random import randgen
from factory.django import DjangoModelFactory
from .models import StudentCard, Student, ATRCardType


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

