from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_csv_rfid', views.upload_rfid, name='upload_rfid')
]
