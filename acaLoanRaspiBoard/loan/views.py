import csv
import io
import datetime
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
	template_name_submitted = "loan/link_boards.html"


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

	rfids_dict = {}
	boards_failed_dict = {}
	rfids_uids_failed_dict = {}
	counter = 0
	for row in csv.reader(io_string, delimiter=','):
		_, createdTag = RaspiTag.objects.update_or_create(
			atr_hex=ATRCardType.RASPI_TAG_ATR,
			uid=row[1]
		)
		"""The update() method adds element(s) to the dictionary if the key is not in the dictionary. 
		If the key is in the dictionary, it updates the key with the new value."""
		# board_no is duplicated
		if row[0] in rfids_dict.keys():
			boards_failed_dict.update({row[0]: row[1]})
		# rfid_tag is duplicated
		if row[1] in rfids_dict.values():
			rfids_uids_failed_dict.update({row[0]: row[1]})
		# everything is okay
		if row[0] not in rfids_dict.keys() and row[1] not in rfids_dict.values():
			rfids_dict.update({row[0]: row[1]})

		counter += 1

	queryset = RaspiTag.objects.all().order_by('-id')[:counter]
	boards_qs = Board.objects.all()
	context = {"csv_uploaded": "True", "boards_uid_list": queryset, "boards": boards_qs, "counter": counter,
				"rfids_dict": rfids_dict, "boards_failed_dict": boards_failed_dict,
				"rfids_uids_failed_dict": rfids_uids_failed_dict}
	return render(request, template_name_submitted, context)

@staff_member_required
def link_boards(request):
	#queryset = RaspiTag.objects.all()
	template_name = "loan/link_boards.html"
	#context = {"boards_uid_list": queryset}
	context = {}
	return render(request, template_name, context)
