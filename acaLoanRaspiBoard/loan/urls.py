from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_rfid', views.upload_rfid, name='upload_rfid'),
    path('link_boards_rfid', views.link_boards, name='link_boards')

]
