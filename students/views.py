from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse

from datetime import date
from django.utils import timezone

import pandas as pd

from .models import Student, Group


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
    data = pd.read_excel(request.FILES['uploaded_students'])
    data = data.astype('str')
    context = {
        'students_to_add' : [],
        'groups_to_add' : [],
        'students_to_delete' : [],
        'students_to_update_group' : [],
        'students_to_add_dob' : [],
    }
    students_to_add = []
    groups_to_add = []
    students_to_delete = []
    students_to_update_group = []
    students_to_add_dob = []
    for index, row in data.iterrows():
        lastname, firstname, middlename, group, dob = row
        if group != '' and group != 'nan':
            try:
                group_num, group_liter = group.split()
                gr = Group.objects.get(
                    num=group_num,
                    liter=group_liter
                )
            except:
                groups_to_add.append({ 'num' : group_num, 'liter' : group_liter})
                context['groups_to_add'].append({ 'num' : group_num, 'liter' : group_liter})
        else:
            gr = None
            group = ''
        
        if dob == 'NaN' or dob == 'NaT' or dob == '':
            dob = None

        try:
            student = Student.objects.get(
                last_name=lastname,
                first_name=firstname,
                middle_name=middlename,
                group=gr
            )
            if student.date_of_birth == None and dob != None:
                students_to_add_dob.append([student.id, lastname, firstname, middlename, group, dob])
                context['students_to_add_dob'].append([student.id, lastname, firstname, middlename, group if group else '', date.fromisoformat(dob) if dob else dob])
        except:
            try:
                student = Student.objects.get(
                    last_name=lastname,
                    first_name=firstname,
                    middle_name=middlename,
                    date_of_birth=dob
                )
                if str(student.group) != group:
                    students_to_update_group.append([student.id, lastname, firstname, middlename, str(student.group), dob, group])
                    context['students_to_update_group'].append([student.id,
                                                                lastname,
                                                                firstname,
                                                                middlename,
                                                                student.group if student.group else '',
                                                                date.fromisoformat(dob) if dob else dob, group])
            except:
                students_to_add.append([lastname, firstname, middlename, group, dob])
                context['students_to_add'].append([lastname,
                                                   firstname,
                                                   middlename,
                                                   group if group else '',
                                                   date.fromisoformat(dob) if dob else dob])


    for student in Student.objects.all():
        if len(
            data[
                (data['last_name'] == student.last_name) &
                (data['first_name'] == student.first_name) &
                (data['middle_name'] == student.middle_name) &
                (data['group'] == str(student.group))
            ]
        ) == 0 and (student.date_of_birth == None or len(
            data[
                (data['last_name'] == student.last_name) &
                (data['first_name'] == student.first_name) &
                (data['middle_name'] == student.middle_name) &
                (data['date_of_birth'] == str(student.date_of_birth))
            ]
        ) == 0):
            students_to_delete.append(student.id)
            context['students_to_delete'].append({'id' : student.id,
                                                  'last_name' : student.last_name,
                                                  'first_name' : student.first_name,
                                                  'middle_name' : student.middle_name,
                                                  'group' : student.group if student.group else '',
                                                  'date_of_birth' : student.date_of_birth if student.date_of_birth else ''})


    request.session['students_to_add'] = students_to_add
    request.session['groups_to_add'] = groups_to_add
    request.session['students_to_delete'] = students_to_delete
    request.session['students_to_update_group'] = students_to_update_group
    request.session['students_to_add_dob'] = students_to_add_dob

    return render(request, 'students/add_file_preview.html', context)

def aff_file_submit(request):
    return render(request, 'students/add_file_submit.html')
