import csv, io
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import StudentGroup, Student, Operation, Board, Action, RaspiTag
from .forms import RaspiTagFormModel

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

	csv_file = request.FILES['file']

	if not csv_file.name.endswith('.csv'):
		messages.error(request, "This is not a csv file!")

	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO(data_set)
	next(io_string)

	for row in csv.reader(io_string, delimiter=','):
		_, createdTag = RaspiTag.objects.update_or_create(
			uid=row[1]
		)


def file_upload_view(request):
	# create objects -> use a form
	form = RaspiTagFormModel(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		form = RaspiTagFormModel()
	template_name = "loan/file_upload.html"
	context = {"form": form}
	return render(request, template_name, context)

