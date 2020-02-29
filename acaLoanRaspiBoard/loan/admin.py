from django.contrib import admin

from .models import Student, Board, Action, StudentCard, RaspiTag, Semester

# Register your models here.
admin.site.register(Student)
admin.site.register(Board)
admin.site.register(Action)
admin.site.register(StudentCard)
admin.site.register(RaspiTag)
admin.site.register(Semester)
