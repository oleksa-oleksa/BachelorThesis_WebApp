from django.contrib import admin

from .models import Student, Board, Action, SemesterList, StudentCard, RaspiTag

# Register your models here.
admin.site.register(Student)
admin.site.register(Board)
admin.site.register(Action)
admin.site.register(SemesterList)
admin.site.register(StudentCard)
admin.site.register(RaspiTag)
