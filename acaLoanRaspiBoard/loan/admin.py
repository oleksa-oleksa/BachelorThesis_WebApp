from django.contrib import admin

from .models import Student, Board, Action, StudentCard, RaspiTag, Semester


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_card', 'semester', 'first_name', 'second_name', 'matricul_no', 'hrz_no',
                    'group', 'is_home_loan_enabled')


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Board)
admin.site.register(Action)
admin.site.register(StudentCard)
admin.site.register(RaspiTag)
admin.site.register(Semester)


