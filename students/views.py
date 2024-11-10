from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from datetime import date
from django.utils import timezone

import pandas as pd

from .models import Student, Group

import students.processing as processing


def index(request):
    students_list = Student.objects.exclude(group__alumnus=True).order_by('group__num', 'group__liter', 'last_name', 'first_name', 'middle_name')
    context = {'students': students_list}
    return render(request, 'students/index.html', context)

def detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'students/detail.html', {'student': student})

def edit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    context = {
        'student' : student,
        'groups_list' : Group.objects.filter(alumnus=False)
    }
    return render(request, 'students/edit.html', context)

def edit_submit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    processing.edit_student(request, student)
    return HttpResponseRedirect(reverse('students:detail', args=(student_id,)))


def add(request):
    context = { 'groups_list' : Group.objects.filter(alumnus=False)}
    return render(request, 'students/add.html', context)

def add_submit(request):
    student = processing.add_student(request)
    return HttpResponseRedirect(reverse('students:detail', args=(student.id,)))

def add_file(request):
    return render(request, 'students/add_file.html')

def add_file_preview(request):
    context = {
        'students_to_add' : [],
        'groups_to_add' : [],
        'students_to_delete' : [],
        'students_to_update_group' : [],
        'students_to_add_dob' : [],
    }
    try:
        processing.get_students_update_lists(request, context)
        return render(request, 'students/add_file_preview.html', context)
    except:
        return render(request, 'students/add_file_error.html')

def add_file_submit(request):
    try:
        processing.save_students_update_lists(request)
        return HttpResponseRedirect(reverse('students:index'))
    except:
        return HttpResponseRedirect(reverse('students:add_file_error'))

def add_file_error(request):
    return render(request, 'students/add_file_error.html')
