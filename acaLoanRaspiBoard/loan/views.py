import csv, io
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import StudentGroup, Student, Operation, Board, Action
from .forms import StudentCardFormModel

"""
def index(request):
	return HttpResponse("Hello, world. You're at the loan index.")
"""


def index(request):
	queryset = Board.objects.all()
	template_name = "loan/index.html"
	context = {"home_boards_list": queryset}
	return render(request, template_name, context)


@staff_member_required
def rfid_upload(request):
	template_name = "loan/rfid_upload.html"

	prompt = {
		'order': 'Order of CSV should be: board_no,  rfid_uid'
	}

	if request.method == "GET":
		return render(request, template_name, prompt)

def file_upload_view(request):
	# create objects -> use a form
	form = StudentCardFormModel(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		form = StudentCardFormModel()
	template_name = "loan/file_upload.html"
	context = {"form": form}
	return render(request, template_name, context)

