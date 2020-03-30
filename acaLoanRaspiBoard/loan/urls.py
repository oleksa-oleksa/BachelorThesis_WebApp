from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_rfid', views.upload_rfid, name='upload_rfid'),
    path('link_boards_rfid', views.link_boards, name='link_boards'),
    path('upload_student', views.upload_student, name='upload_student'),
    path('link_student_card', views.link_students, name='link_students'),
    path('admin', views.admin_page, name='admin')

]
