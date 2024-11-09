from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from datetime import date
from django.utils import timezone

import pandas as pd

from .models import Student, Group

from .processing import get_students_update_lists, save_students_update_lists


def index(request):
    students_list = Student.objects.exclude(group__alumnus=True).order_by('group__num', 'group__liter', 'last_name', 'first_name', 'middle_name')
    context = {'students': students_list}
    return render(request, 'students/index.html', context)

def detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'students/detail.html', {'student': student})

def edit(request, student_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % student_id)

def add(request):
    return HttpResponse("All good!")

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
    # try:
    get_students_update_lists(request, context)
    return render(request, 'students/add_file_preview.html', context)
    # except:
    #     return render(request, 'students/add_file_error.html')

def add_file_submit(request):
    try:
        save_students_update_lists(request)
        return HttpResponseRedirect(reverse('students:index'))
    except:
        assert False
        return HttpResponseRedirect(reverse('students:add_file_error'))

def add_file_error(request):
    return render(request, 'students/add_file_error.html')
