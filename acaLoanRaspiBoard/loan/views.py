from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import StudentGroup, Student, Operation, Board, Action

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
def file_upload_view(request):
	# create objects -> use a form
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		# obj = BlogPost.objects.create(**form.cleaned_data)
		obj = form.save(commit=False)
		# obj.title = form.cleaned_data.get("title")
		obj.user = request.user
		obj.save()
		form = BlogPostModelForm()
	template_name = "blog/form.html"
	context = {"form": form}
	return render(request, template_name, context)

