from django.contrib import admin

from .models import Student, Board, Action, StudentCard, RaspiTag, Semester, Session


class StudentAdmin(admin.ModelAdmin):
    list_display = ('second_name', 'first_name', 'matricul_no', 'hrz_no', 'semester', 'student_card',
                    'group', 'is_home_loan_enabled')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('board_no', 'board_type', 'board_status', 'raspi_tag')


class ActionAdmin(admin.ModelAdmin):
    list_display = ('student', 'board',  'timestamp',  'operation')


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semester']


class StudentCardAdmin(admin.ModelAdmin):
    list_display = ('atr_hex', 'uid', 'student')

    def student(self, obj):
        return obj.student.second_name + obj.student.first_name


class RaspiTagAdmin(admin.ModelAdmin):
    list_display = ('atr_hex', 'uid', 'board')

    def board(self, obj):
        return obj.board.board_no + obj.board.board_type + 'is ' + obj.board.board_status


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'state')


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(StudentCard, StudentCardAdmin)
admin.site.register(RaspiTag, RaspiTagAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Session, SessionAdmin)



