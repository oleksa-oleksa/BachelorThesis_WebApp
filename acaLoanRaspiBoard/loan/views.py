from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import StudentGroup, Student, Operation, Board, Action

"""
def index(request):
	return HttpResponse("Hello, world. You're at the loan index.")
"""


def index(request):
	return render(request, "loan/index.html")
