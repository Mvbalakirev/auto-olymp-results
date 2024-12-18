from datetime import date
from django.utils import timezone
from django.db.models import Max
from django.forms.models import model_to_dict
import openpyxl

from copy import copy, deepcopy
import pandas as pd
from . import signals

from students.models import *
from .models import *

from django.shortcuts import get_object_or_404

def stages_file(f, olymp):
    df = pd.read_excel(f, sheet_name=None)
    for stage_name, data in df.items():
        data = data.fillna('').astype('str')
        for col in data.columns:
            data[col] = data[col].str.strip(' ')

        try:
            stage = OlympStage.objects.get(olymp=olymp, name=stage_name)
        except:
            qs = OlympStage.objects.filter(olymp=olymp)
            if len(qs) > 0:
                mxnum = qs.aggregate(Max('num'))['num__max']
            else:
                mxnum = 0
            stage = OlympStage(olymp=olymp, name=stage_name, num=mxnum + 1)
            stage.save()
        for index, row in data.iterrows():
            subject = Subject.objects.get(name=row['subject'])
            try:
                stage_subject = OlympStageSubject.objects.get(stage=stage, subject=subject)
            except:
                stage_subject = OlympStageSubject(stage=stage, subject=subject)
            stage_subject.min_class = int(row['min_class'])
            stage_subject.max_class = int(row['max_class'])
            if row['date'] != '' and row['date'].lower() != 'nan' and row['date'].lower() != 'nat':
                stage_subject.date = row['date']
            else:
                stage_subject.date = None
            stage_subject.save()

def get_applications_update_lists(request, context, subject, checks):
    data = pd.read_excel(request.FILES['file'])
    data = data.fillna('').astype('str')
    for col in data.columns:
        data[col] = data[col].str.strip(' ')
    for index, row in data.iterrows():
        item = {
            'last_name' : row['last_name'],
            'first_name' : row['first_name'],
            'middle_name' : row['middle_name'],
            'parallel' : row['parallel'],
            'group' : row['group'],
            'code' : row['code'],
            'result' : row['result'],
            'status' : row['status'],
        }
        
        if item['last_name'] is None or not(item['last_name'] != '' and item['last_name'].lower() != 'nan' and item['last_name'].lower() != 'nat'):
            item['last_name'] = None
        
        if item['first_name'] is None or not(item['first_name'] != '' and item['first_name'].lower() != 'nan' and item['first_name'].lower() != 'nat'):
            item['first_name'] = None

        if item['middle_name'] is None or not(item['middle_name'] != '' and item['middle_name'].lower() != 'nan' and item['middle_name'].lower() != 'nat'):
            item['middle_name'] = None

        if item['parallel'] is None or not(item['parallel'] != '' and item['parallel'].lower() != 'nan' and item['parallel'].lower() != 'nat'):
            item['parallel'] = None
        else:
            item['parallel'] = int(float(item['parallel']))
        
        if item['code'] is None or not(item['code'] != '' and item['code'].lower() != 'nan' and item['code'].lower() != 'nat'):
            item['code'] = None
        
        if item['result'] is None or not(item['result'] != '' and item['result'].lower() != 'nan' and item['result'].lower() != 'nat'):
            item['result'] = None
        else:
            item['result'] = float(item['result'].replace(',', '.'))
        
        if item['status'] is None or not(item['status'] != '' and item['status'].lower() != 'nan' and item['status'].lower() != 'nat'):
            item['status'] = None

        if item['group'] is None or not(item['group'] != '' and item['group'].lower() != 'nan' and item['group'].lower() != 'nat'):
            item['group'] = None
        else:
            try:
                num, liter = item['group'].split()
                int(num)
                item['group'] = num + ' ' + liter
            except:
                item['comment'] = 'Некорректно указан класс'
                context['errors'].append(item)
                continue
        
        

        if item['status'] is None or not(item['status'] != '' and item['status'].lower() != 'nan' and item['status'].lower() != 'nat'):
            item['status'] = ''

        if item['status'] not in Status.labels and item['status'] != '':
            item['comment'] = 'Некорректный статус'
            context['errors'].append(item)
            continue

        if item['last_name'] is None or item['first_name'] is None:
            item['comment'] = 'Не указаны имя или фамилия'
            context['errors'].append(item)
            continue
        
        students = Student.objects.all().filter(last_name=item['last_name'], first_name=item['first_name'])
        
        if checks['middle_name'] and item['middle_name'] is not None:
            students = students.filter(middle_name=item['middle_name'])
        
        if checks['group'] and item['group'] is not None:
            try:
                num, liter = item['group'].split()
                group = Group.objects.get(num=int(num), liter=liter)
            except:
                item['comment'] = 'Не найден класс в базе'
                context['errors'].append(item)
                continue
            students = students.filter(group=group)
        
        if not checks['alumnus']:
            students = students.exclude(group__alumnus=True)
        
        if len(students) < 1:
            item['comment'] = 'Ученик не найден'
            context['errors'].append(item)
            continue
        if len(students) > 1:
            item['comment'] = 'Найдено более одного ученика'
            context['errors'].append(item)
            continue

        student = students[0]
        if student.group is not None and item['group'] is None:
            item['group'] = str(student.group)
            group = student.group

        if student.group is not None and item['parallel'] is None:
            item['parallel'] = max(student.group.num, subject.min_class)

        if item['parallel'] < subject.min_class or item['parallel'] > subject.max_class:
            item['comment'] = 'Некорректная параллель'
            context['errors'].append(item)
            continue

        try:
            oldapp = Application.objects.get(stage_subject=subject, student=student)
            app = copy(oldapp)
            app.parallel = item['parallel']
            app.group = item['group']
            app.code = item['code']
            app.result = item['result']
            for el in Status:
                if item['status'] == el.label:
                    app.status = el
                    break
                app.status = None
            
            if model_to_dict(oldapp) != model_to_dict(app):
                context['to_update'].append({
                    'old' : oldapp,
                    'new' : app,
                })
            else:
                context['no_change'].append(app)
        except:
            app = Application(stage_subject=subject, student=student)
            app.parallel = item['parallel']
            app.group = item['group']
            app.code = item['code']
            app.result = item['result']
            for el in Status:
                if item['status'] == el.label:
                    app.status = el
                    break
                app.status = None
            context['to_add'].append(app)
        request.session['to_add'] = [model_to_dict(x) for x in context['to_add']]
        request.session['to_update'] = [model_to_dict(x['new']) for x in context['to_update']]


def save_applications_update_lists(request, subject):
    to_add = request.session.get('to_add')
    to_update = request.session.get('to_update')
    request.session.pop('to_add')
    request.session.pop('to_update')
    
    if 'is_add' in request.POST:
        for data in to_add:
            try:
                data['stage_subject_id'] = data.pop('stage_subject')
                data['student_id'] = data.pop('student')
                Application(**data).save()
            except:
                pass
    
    if 'is_update' in request.POST:
        for data in to_update:
            try:
                data['stage_subject_id'] = data.pop('stage_subject')
                data['student_id'] = data.pop('student')
                Application(**data).save()
            except:
                pass
def create_excel(data_sheets, filename='export.xlsx'):
    excel_writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    for sheetname, data in data_sheets.items():
        df = pd.DataFrame(data).rename(columns={
            'last_name' : 'Фамилия',
            'first_name' :'Имя',
            'middle_name' : 'Отчество',
            'code' : 'Код',
            'parallel' : 'Параллель',
            'group' : 'Класс',
            'result' : 'Баллы',
            'status' : 'Статус',
        })
        df.to_excel(excel_writer, sheet_name=sheetname)
    excel_writer.close()