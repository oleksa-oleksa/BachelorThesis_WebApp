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


class RaspiTagAdmin(admin.ModelAdmin):
    list_display = ('atr_hex', 'uid', 'board')

    def board(self, obj):
        return obj.board.board_no + obj.board.board_type + 'is ' + obj.board.board_status


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_card', 'student_name', 'board_no', 'start_time', 'state')

    def student_name(self, obj):
        if obj.student_card is None:
            return "None"

        student = obj.student_card.student
        return "{} {}".format(student.second_name, student.first_name)

    def board_no(self, obj):
        if obj.raspi_tag is None:
            return "None"

        return "{}".format(obj.raspi_tag.board.board_no)


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(StudentCard, StudentCardAdmin)
admin.site.register(RaspiTag, RaspiTagAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Session, SessionAdmin)



