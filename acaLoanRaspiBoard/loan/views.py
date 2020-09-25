import csv
import io
import datetime
import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django_fsm import TransitionNotAllowed
from .models import StudentCard, Student, Operation, Board, Action, RaspiTag, ATRCardType, Session
from .constraint import *
from .serializers import render_session

@csrf_exempt
def sessions_list(request):
    if request.method == "POST":
        session = Session()
        try:
            session.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=403, safe=False)
        session.save()
        return JsonResponse(model_to_dict(session), status=201, safe=False)


@csrf_exempt
def events(request):
    if request.method != "POST":
        return HttpResponseNotFound()

    session = Session.get_active_session()

    if session is None:
        return HttpResponseBadRequest()
    print(request.body)
    # type, uid
    try:
        body = json.loads(request.body)
        input_type = body['type']
        print("type:", input_type)

    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest()

    if input_type not in ["card", "tag", "cancel_button", "terminate_button", "get_rfid_status",
                          "return_scanned_board_button", "loan_scanned_board_button", "finish_button"]:
        return HttpResponseBadRequest()

    try:
        if input_type == "card":
            try:
                uid = body['uid']
                session.student_card_inserted(uid)
            except StudentCard.DoesNotExist:
                pass
        elif input_type == "tag":
            uid = body['uid']
            session.rfid_inserted(uid)

        elif input_type == "cancel_button":
            session.session_canceled()

        elif input_type == "finish_button":
            session.session_finished()

        elif input_type == "get_rfid_status":
            session.get_rfid_status()

        elif input_type == "return_scanned_board_button":
            session.loaned_board_returned()

        elif input_type == "loan_scanned_board_button":
            session.loan_active_board()

        elif input_type == "terminate_button":
            session.session_terminated()

    except TransitionNotAllowed:
        return HttpResponseNotAllowed()

    session.save()

    return JsonResponse(model_to_dict(session), status=201, safe=False)


@csrf_exempt
def session_state(request, session_id):
    # we receive GET /api/sessions/id
    if request.method == "GET":
        current_session = Session.get_active_session()

        if current_session is None:
            return HttpResponseNotFound()

        elif current_session is not None and current_session.id == session_id:
            session_dict = render_session(current_session)
            return JsonResponse(session_dict, status=201, safe=False)

        else:
            return HttpResponseNotFound()

    else:
        return HttpResponseNotFound()


def index(request):
    queryset = Board.objects.filter(board_no__gte=HOME_LOAN_MINIMAL_NO)
    template_name = "loan/index.html"
    context = {"home_boards_list": queryset}
    return render(request, template_name, context)


def start(request):
    queryset = Board.objects.filter(board_no__gte=HOME_LOAN_MINIMAL_NO)
    template_name = "loan/start.html"
    # session = Session.get_active_session()
    #
    # if session is None:
    # 	session = Session()
    # 	session.save()

    context = {"home_boards_list": queryset}
    return render(request, template_name, context)


@staff_member_required
def admin_page(request):
    template_name = "loan/admin_page.html"
    context = {}
    return render(request, template_name, context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


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
        created_tag, _ = RaspiTag.objects.update_or_create(
            atr_hex=ATRCardType.RASPI_TAG_ATR,
            uid=row[1]
        )
        """The update() method adds element(s) to the dictionary if the key is not in the dictionary. 
        If the key is in the dictionary, it updates the key with the new value."""

        # board_no is duplicated
        if row[0] in rfids_dict.keys():
            if row[0] not in boards_failed_dict.keys():
                boards_failed_dict[row[0]] = [row[1]]
            else:
                boards_failed_dict[row[0]].append(row[1])

        # rfid_tag is duplicated
        if row[1] in rfids_dict.values():
            if row[1] not in rfids_uids_failed_dict.keys():
                rfids_uids_failed_dict[row[1]] = [row[0]]
            else:
                rfids_uids_failed_dict[row[1]].append(row[0])
        # everything is okay
        if row[0] not in rfids_dict.keys() and row[1] not in rfids_dict.values():
            rfids_dict.update({row[0]: row[1]})
            Board.objects.filter(board_no=row[0]).update(raspi_tag=created_tag)

        counter += 1

    # select * from raspi_tag order by id desc
    # seelct * from raspi_tag join boards on raspitag.id = boards.rapbitag_id
    queryset = RaspiTag.objects.select_related('board').all().order_by('-id')[:counter]

    context = {"csv_uploaded": "True", "queryset": queryset, "counter": counter,
               "rfids_dict": rfids_dict, "boards_failed_dict": boards_failed_dict,
               "rfids_uids_failed_dict": rfids_uids_failed_dict}
    return render(request, template_name_submitted, context)


@staff_member_required
def link_boards(request):
    template_name = "loan/link_boards.html"
    context = {}
    return render(request, template_name, context)


@staff_member_required
def upload_student(request):
    template_name = "loan/upload_student.html"
    template_name_submitted = "loan/link_students.html"


    prompt = {
        'order': 'Order of CSV should be: matricul_no,  card_uid'
    }

    if request.method == "GET":
        return render(request, template_name, prompt)

    csv_file = request.FILES['student_list']

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

    cards_dict = {}
    student_failed_dict = {}
    cards_uids_failed_dict = {}
    counter = 0
    for row in csv.reader(io_string, delimiter=','):
        created_card, _ = StudentCard.objects.update_or_create(
            atr_hex=ATRCardType.STUDENT_CARD_ATR,
            uid=row[1]
        )
        """The update() method adds element(s) to the dictionary if the key is not in the dictionary. 
        If the key is in the dictionary, it updates the key with the new value."""

        # board_no is duplicated
        if row[0] in cards_dict.keys():
            if row[0] not in student_failed_dict.keys():
                student_failed_dict[row[0]] = [row[1]]
            else:
                student_failed_dict[row[0]].append(row[1])

        # rfid_tag is duplicated
        if row[1] in cards_dict.values():
            if row[1] not in cards_uids_failed_dict.keys():
                cards_uids_failed_dict[row[1]] = [row[0]]
            else:
                cards_uids_failed_dict[row[1]].append(row[0])
        # everything is okay
        if row[0] not in cards_dict.keys() and row[1] not in cards_dict.values():
            cards_dict.update({row[0]: row[1]})
            Student.objects.filter(matricul_no=row[0]).update(student_card=created_card)

        counter += 1

    # select * from raspi_tag order by id desc
    # seelct * from raspi_tag join boards on raspitag.id = boards.rapbitag_id
    queryset = StudentCard.objects.select_related('student').all().order_by('-id')[:counter]

    context = {"csv_uploaded": "True", "queryset": queryset, "counter": counter,
               "cards_dict": cards_dict, "student_failed_dict": student_failed_dict,
               "cards_uids_failed_dict": cards_uids_failed_dict}
    return render(request, template_name_submitted, context)


@staff_member_required
def link_students(request):
    template_name = "loan/link_students.html"
    context = {}
    return render(request, template_name, context)
