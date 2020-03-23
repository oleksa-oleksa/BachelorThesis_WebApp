import csv, io
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import StudentGroup, Student, Operation, Board, Action, RaspiTag, ATRCardType
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
def upload_rfid(request):
	template_name = "loan/upload_rfid.html"

	prompt = {
		'order': 'Order of CSV should be: board_no,  rfid_uid'
	}

	if request.method == "GET":
		return render(request, template_name, prompt)

	csv_file = request.FILES['rfid_list']

	if not csv_file.name.endswith('.csv'):
		messages.error(request, "This is not a csv file!")

	if csv_file.multiple_chunks():
		messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
		return render(request, template_name, prompt)

	data_set = csv_file.read().decode('UTF-8')
	"""In-memory text streams are also available as StringIO objects:"""
	io_string = io.StringIO(data_set)
	# admin_get_boards.py creates csv-file without header (there is no need, file contains only two columns)
	# next(io_string)

	for row in csv.reader(io_string, delimiter=','):
		_, createdTag = RaspiTag.objects.update_or_create(
			atr_hex=ATRCardType.RASPI_TAG_ATR,
			uid=row[1]
		)

	context = {}
	return render(request, template_name, context)

