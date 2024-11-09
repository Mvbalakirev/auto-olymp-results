from datetime import date
from django.utils import timezone

import pandas as pd

from .models import Student, Group

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
        if group != '' and group != 'nan':
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
                groups_to_add.append({ 'num' : group_num, 'liter' : group_liter})
                context['groups_to_add'].append({ 'num' : group_num, 'liter' : group_liter})
        else:
            gr = None
            group = ''
        
        if dob == 'NaN' or dob == 'NaT' or dob == '':
            dob = None
        if middlename == 'NaN' or middlename == 'NaT' or middlename == '':
            middlename = None


        try:
            student = Student.objects.get(
                last_name=lastname,
                first_name=firstname,
                middle_name=middlename,
                group=gr
            )
            if student.date_of_birth == None and dob != None:
                students_to_add_dob.append([student.id, lastname, firstname, middlename, group, dob])
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
                    students_to_update_group.append([student.id, lastname, firstname, middlename, str(student.group), dob, group])
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
                                                  'group' : student.group,
                                                  'date_of_birth' : student.date_of_birth if student.date_of_birth else ''})


    request.session['students_to_add'] = students_to_add
    request.session['groups_to_add'] = groups_to_add
    request.session['students_to_delete'] = students_to_delete
    request.session['students_to_update_group'] = students_to_update_group
    request.session['students_to_add_dob'] = students_to_add_dob