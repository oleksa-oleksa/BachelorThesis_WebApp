from django.contrib import admin

from .models import Student, Board, Action, StudentCard, RaspiTag, Semester


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_card', 'semester', 'first_name', 'second_name', 'matricul_no', 'hrz_no',
                    'group', 'is_home_loan_enabled')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('raspi_tag', 'board_no',  'board_type',  'board_status',)


class ActionAdmin(admin.ModelAdmin):
    list_display = ('student', 'board',  'timestamp',  'operation',)


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semester']


class StudentCardAdmin(admin.ModelAdmin):
    list_display = ('atr_hex', 'uid', 'student')

    def student(self, obj):
        return obj.student.second_name + obj.student.first_name


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(StudentCard, StudentCardAdmin)
admin.site.register(RaspiTag)
admin.site.register(Semester, SemesterAdmin)


