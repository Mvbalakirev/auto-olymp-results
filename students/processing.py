from datetime import date
from django.utils import timezone

import pandas as pd

from .models import Student, Group
from django.shortcuts import get_object_or_404

def get_students_update_lists(request, context):
    data = pd.read_excel(request.FILES['uploaded_students'])
    data = data.fillna('').astype('str')
    for col in data.columns:
        data[col] = data[col].str.strip(' ')
    students_to_add = []
    groups_to_add = []
    students_to_delete = []
    students_to_update_group = []
    students_to_add_dob = []
    for index, row in data.iterrows():
        lastname, firstname, middlename, group, dob = row
        if group != '' and group.lower() != 'nan':
            try:
                group_num, group_liter = group.split()
                gr = Group.objects.get(
                    num=group_num,
                    liter=group_liter
                )
            except:
                gr = Group(
                    num=group_num,
                    liter=group_liter
                )
                if (group_num, group_liter) not in groups_to_add:
                    groups_to_add.append((group_num, group_liter))
                    context['groups_to_add'].append({ 'num' : group_num, 'liter' : group_liter})
        else:
            gr = None
            group = None
        
        if dob.lower() == 'nan' or dob.lower() == 'nat' or dob == '':
            dob = None
        if middlename.lower() == 'nan' or middlename.lower() == 'nat' or middlename == '':
            middlename = None


        try:
            student = Student.objects.get(
                last_name=lastname,
                first_name=firstname,
                middle_name=middlename,
                group=gr
            )
            if student.date_of_birth == None and dob != None:
                students_to_add_dob.append([student.id, dob])
                context['students_to_add_dob'].append([student.id, lastname, firstname, middlename, gr, date.fromisoformat(dob) if dob else dob])
        except:
            try:
                student = Student.objects.get(
                    last_name=lastname,
                    first_name=firstname,
                    middle_name=middlename,
                    date_of_birth=dob
                )
                if str(student.group) != group:
                    students_to_update_group.append([student.id, group])
                    context['students_to_update_group'].append([student.id,
                                                                lastname,
                                                                firstname,
                                                                middlename,
                                                                student.group,
                                                                date.fromisoformat(dob) if dob else dob, group])
            except:
                students_to_add.append([lastname, firstname, middlename, group, dob])
                context['students_to_add'].append([lastname,
                                                   firstname,
                                                   middlename,
                                                   gr,
                                                   date.fromisoformat(dob) if dob else dob])


    for student in Student.objects.all():
        if student.group and student.group.alumnus == True:
            continue
        if len(
            data[
                (data['last_name'] == student.last_name) &
                (data['first_name'] == student.first_name) &
                (data['middle_name'] == (student.middle_name if student.middle_name else '')) &
                (data['group'] == (str(student.group) if student.group else ''))
            ]
        ) == 0 and (student.date_of_birth == None or len(
            data[
                (data['last_name'] == student.last_name) &
                (data['first_name'] == student.first_name) &
                (data['middle_name'] == (student.middle_name if student.middle_name else '')) &
                (data['date_of_birth'] == (str(student.date_of_birth) if student.date_of_birth else ''))
            ]
        ) == 0):
            students_to_delete.append(student.id)
            context['students_to_delete'].append({'id' : student.id,
                                                  'last_name' : student.last_name,
                                                  'first_name' : student.first_name,
                                                  'middle_name' : student.middle_name,
                                                  'group' : student.group,
                                                  'date_of_birth' : student.date_of_birth if student.date_of_birth else ''})


    request.session['students_to_add'] = students_to_add
    request.session['groups_to_add'] = groups_to_add
    request.session['students_to_delete'] = students_to_delete
    request.session['students_to_update_group'] = students_to_update_group
    request.session['students_to_add_dob'] = students_to_add_dob

def save_students_update_lists(request):
    students_to_add = request.session.get('students_to_add')
    groups_to_add = request.session.get('groups_to_add')
    students_to_delete = request.session.get('students_to_delete')
    students_to_update_group = request.session.get('students_to_update_group')
    students_to_add_dob = request.session.get('students_to_add_dob')

    request.session.pop('students_to_add')
    request.session.pop('groups_to_add')
    request.session.pop('students_to_delete')
    request.session.pop('students_to_update_group')
    request.session.pop('students_to_add_dob')

    is_delete = False
    try:
        if request.POST['is_delete'] == "Yes":
            is_delete = True
    except:
        pass

    newgroups = []

    for num, liter in groups_to_add:
        newgroups.append(Group(num=num, liter=liter))
    Group.objects.bulk_create(newgroups)


    newstudents = []

    for lastname, firstname, middlename, group, dob in students_to_add:
        if group:
            num, liter = group.split()
            gr = Group.objects.get(num=int(num), liter=liter)
        else:
            gr = None
        newstudents.append(Student(
            last_name=lastname,
            first_name=firstname,
            middle_name=middlename,
            group=gr,
            date_of_birth=dob
        ))
    Student.objects.bulk_create(newstudents)
    
    for id, dob in students_to_add_dob:
        student = Student.objects.get(pk=id)
        student.date_of_birth = dob
        student.save()
    
    for id, group in students_to_update_group:
        if group:
            num, liter = group.split()
            gr = Group.objects.get(num=num, liter=liter)
        else:
            gr = None
        student = Student.objects.get(pk=id)
        student.group = gr
        student.save()
    
    if is_delete:
        for id in students_to_delete:
            Student.objects.get(pk=id).delete()

def add_student(request):
    try:
        group_num, group_liter = request.POST['group'].strip(' ').split()
        try:
            group = Group.objects.get(num=int(group_num), liter=group_liter)
        except:
            group = Group(num=int(group_num), liter=group_liter)
            group.save()
    except:
        group = None

    student = Student(
        last_name=request.POST['last_name'].strip(' '),
        first_name=request.POST['first_name'].strip(' '),
        middle_name=(request.POST['middle_name'].strip(' ') if request.POST['middle_name'] != '' else None),
        group=group,
        date_of_birth=(request.POST['date_of_birth'].strip(' ') if request.POST['date_of_birth'] != '' else None),
    )
    student.save()
    return student

def edit_student(request, student):
    try:
        group_num, group_liter = request.POST['group'].strip(' ').split()
        try:
            group = Group.objects.get(num=int(group_num), liter=group_liter)
        except:
            group = Group(num=int(group_num), liter=group_liter)
            group.save()
    except:
        group = None
    
    student.last_name = request.POST['last_name'].strip(' ')
    student.first_name = request.POST['first_name'].strip(' ')
    student.middle_name = (request.POST['middle_name'].strip(' ') if request.POST['middle_name'] != '' else None)
    student.group = group
    student.date_of_birth = (request.POST['date_of_birth'].strip(' ') if request.POST['date_of_birth'] != '' else None)
    student.save()
