from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from copy import copy, deepcopy
from django.db.models import Q

from datetime import date
from django.utils import timezone

import pandas as pd
from transliterate import translit

from students.models import *
from .models import *
from .forms import *
import olymps.processing as processing

def index(request):
    olymps_list = Olymp.objects.all()
    context = {'olymps': olymps_list}
    return render(request, 'olymps/index.html', context)

def detail(request, olymp_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stages = olymp.olympstage_set.all().order_by('num')
    context = {
        'olymp' : olymp,
        'stages' : stages
    }
    return render(request, 'olymps/detail.html', context)

def edit(request, olymp_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stages = olymp.olympstage_set.all().order_by('num')
    context = {
        'olymp' : olymp,
        'stages' : stages,
        'form' : OlympForm(instance=olymp),
        'form_stage' : OlympStageFormset(prefix='stage', queryset=stages),
    }

    if request.method == 'POST':
        form = OlympForm(request.POST, instance=olymp)
        formset = OlympStageFormset(request.POST, prefix='stage')
        if form.is_valid() and formset.is_valid():
            try:
                olymp = form.save(commit=True)
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:detail', args=(olymp.id,)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")

    return render(request, 'olymps/edit.html', context)

def delete(request, olymp_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)

    if request.method == 'POST':
        try:
            olymp.delete()
            HttpResponseRedirect(reverse('olymps:index'))
        except:
            return HttpResponse("Произошла ошибка")

    return HttpResponseRedirect(reverse('olymps:index'))

def add(request):
    if request.method == "POST":
        form = OlympForm(request.POST)
        if form.is_valid():
            try:
                olymp = form.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:detail', args=(olymp.id,)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")
    else:
        context = {
            'form' : OlympForm(),
        }
        return render(request, 'olymps/add.html', context)

def stage_delete(request, olymp_id, stage_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)

    if request.method == 'POST':
        try:
            stage.delete()
            HttpResponseRedirect(reverse('olymps:index'))
        except:
            return HttpResponse("Произошла ошибка")

    return HttpResponseRedirect(reverse('olymps:stage_detail', args=(olymp_id, stage_id,)))

def stage_add(request, olymp_id):
    if request.method == "POST":
        form = StageForm(request.POST)
        if form.is_valid():
            try:
                stage = form.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:stage_detail', args=(stage.olymp.id, stage.id)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")
    else:
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        context = {
            'olymp' : olymp,
            'form' : StageForm(instance=OlympStage(olymp=olymp)),
        }
        return render(request, 'olymps/stage/add.html', context)


def stage_add_file(request, olymp_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    if request.method == "POST":
        try:
            f = request.FILES['file']
            processing.stages_file(f, olymp)
            return HttpResponseRedirect(reverse('olymps:detail', args=(olymp.id,)))
        except:
            return HttpResponse("Произошла ошибка")
    else:
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        context = {
            'olymp' : olymp,
        }
        return render(request, 'olymps/stage/add_file.html', context)

def stage_detail(request, olymp_id, stage_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subjects = stage.olympstagesubject_set.all().order_by('-date', 'subject__name')
    context = {
        'stage' : stage,
        'stage_subjects' : subjects
    }
    return render(request, 'olymps/stage/detail.html', context)

def stage_edit(request, olymp_id, stage_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subjects = stage.olympstagesubject_set.all().order_by('subject__name')
    
    context = {
        'olymp' : olymp,
        'stage' : stage,
        'subjects' : subjects,
        'form' : StageForm(instance=stage),
        'form_subject' : StageSubjectsFormset(prefix='subject', queryset=subjects),
    }

    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        formset = StageSubjectsFormset(request.POST, prefix='subject')
        if form.is_valid() and formset.is_valid():
            try:
                stage = form.save(commit=True)
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:stage_detail', args=(stage.olymp.id, stage.id,)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")

    return render(request, 'olymps/stage/edit.html', context)

def stage_delete(request, olymp_id, stage_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    if request.method == 'POST':
        try:
            stage.delete()
            return HttpResponseRedirect(reverse('olymps:detail', args=(olymp_id,)))
        except:
            return HttpResponse('Произошла ошибка')
    else:
        return HttpResponse('Некорректный метод запроса')


def stage_subject_add(request, olymp_id, stage_id):
    if request.method == "POST":
        form = StageSubjectForm(request.POST)
        if form.is_valid():
            try:
                stage_subject = form.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:stage_detail', args=(stage_subject.stage.olymp.id, stage_subject.stage.id)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")
    else:
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        context = {
            'olymp' : olymp,
            'stage' : stage,
            'form' : StageSubjectForm(instance=OlympStageSubject(stage=stage)),
        }
        return render(request, 'olymps/stage/subject/add.html', context)


def stage_subject_edit(request, olymp_id, stage_id, stage_subject_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    if request.method == "POST":
        form = StageSubjectForm(request.POST, instance=subject)
        if form.is_valid():
            try:
                stage_subject = form.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:stage_subject_detail', args=(stage_subject.stage.olymp.id, stage_subject.stage.id, stage_subject.id)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")
    else:
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        context = {
            'subject' : subject,
            'form' : StageSubjectForm(instance=subject),
        }
        return render(request, 'olymps/stage/subject/edit.html', context)


def stage_subject_delete(request, olymp_id, stage_id, stage_subject_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    if request.method == 'POST':
        try:
            subject.delete()
            return HttpResponseRedirect(reverse('olymps:stage_detail', args=(olymp_id, stage_id)))
        except:
            return HttpResponse('Произошла ошибка')
    else:
        return HttpResponse('Некорректный метод запроса')


def stage_subject_detail(request, olymp_id, stage_id, stage_subject_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    applications = subject.application_set.all().order_by('parallel', 'status', '-result', 'group', 'student__last_name', 'student__first_name', 'student__middle_name')
    context = {
        'subject' : subject,
        'applications' : applications,
        'parallels' : list(range(subject.min_class, subject.max_class + 1)) if subject.min_class <= subject.max_class else None,
    }
    return render(request, 'olymps/stage/subject/detail.html', context)


def stage_subject_parallel(request, olymp_id, stage_id, stage_subject_id, parallel):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    if not(subject.min_class <= parallel and parallel <= subject.max_class):
        return HttpResponseNotFound()
    applications = subject.application_set.filter(parallel=parallel).order_by('status', '-result')
    context = {
        'subject' : subject,
        'applications' : applications,
        'parallels' : list(range(subject.min_class, subject.max_class + 1)) if subject.min_class <= subject.max_class else None,
        'parallel' : parallel,
        'grade' : subject.grade_set.get(parallel=parallel),
        'prev_num' : olymp.olympstage_set.filter(num=stage.num - 1).exists(),
        'prev_year' : Olymp.objects.filter(name=olymp.name, year=olymp.year - 1).exists(),
    }
    return render(request, 'olymps/stage/subject/parallel.html', context)

def export_results(request, olymp_id, stage_id, stage_subject_id=None):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    if stage_subject_id is not None:
        subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
        applications = subject.application_set.all().order_by('parallel', 'status', '-result', 'group', 'student__last_name', 'student__first_name', 'student__middle_name')
    else:
        applications = Application.objects.filter(stage_subject__stage=stage).order_by('stage_subject__subject__name', 'parallel', 'status', '-result', 'group', 'student__last_name', 'student__first_name', 'student__middle_name')
    data = {}
    data['Все'] = []
    for app in applications:
        if stage_subject_id is not None:
            data['Все'].append({
            'Фамилия' : app.student.last_name,
            'Имя' : app.student.first_name,
            'Отчество' : app.student.middle_name,
            'Код' : app.code,
            'Параллель' : app.parallel,
            'Класс' : app.group,
            'Баллы' : app.result,
            'Статус' : app.get_status_display(),
        })
        else:
            data['Все'].append({
                'Предмет' : app.stage_subject.subject.name,
                'Фамилия' : app.student.last_name,
                'Имя' : app.student.first_name,
                'Отчество' : app.student.middle_name,
                'Код' : app.code,
                'Параллель' : app.parallel,
                'Класс' : app.group,
                'Баллы' : app.result,
                'Статус' : app.get_status_display(),
            })
        
    if stage_subject_id is not None:
        for parallel in range(subject.min_class, subject.max_class + 1):
            sheetname = str(parallel) + ' класс'
            data[sheetname] = []
            applications_parallel = applications.filter(parallel=parallel)
            for app in applications_parallel:
                data[sheetname].append({
                    'Фамилия' : app.student.last_name,
                    'Имя' : app.student.first_name,
                    'Отчество' : app.student.middle_name,
                    'Код' : app.code,
                    'Параллель' : app.parallel,
                    'Класс' : app.group,
                    'Баллы' : app.result,
                    'Статус' : app.get_status_display(),
                })
    fn = translit(subject.subject.name, 'ru', reversed=True) if stage_subject_id is not None else translit(stage.name, 'ru', reversed=True)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f"attachment; filename={fn}.xlsx"
    processing.create_excel(data, response)
    
    return response


def export_for_application(request, olymp_id, stage_id, stage_subject_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    applications = subject.application_set.all().order_by('parallel', 'status', '-result', 'group', 'student__last_name', 'student__first_name', 'student__middle_name')
    data = {}
    data['Муниципальный'] = []
    for app in applications:
        data['Муниципальный'].append({
            'Фамилия' : app.student.last_name,
            'Имя' : app.student.first_name,
            'Отчество' : app.student.middle_name,
            'Параллель' : app.parallel,
            'ОУ' : 'ОГАОУ "Шуховский лицей"'
        })

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f"attachment; filename={translit(subject.subject.name, 'ru', reversed=True)}_application.xlsx"
    processing.create_excel(data, response)
    
    return response


def export_participants(request, olymp_id, stage_id, stage_subject_id=None):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    if stage_subject_id is not None:
        subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
        applications = subject.application_set.all().order_by('parallel', 'group__num', 'group__liter', 'student__last_name', 'student__first_name', 'student__middle_name')
    else:
        applications = Application.objects.filter(stage_subject__stage=stage).order_by('stage_subject__subject__name', 'parallel', 'group__num', 'group__liter', 'student__last_name', 'student__first_name', 'student__middle_name')
    data = {}
    data['Все'] = []
    for app in applications:
        if stage_subject_id is not None:
            data['Все'].append({
                'Фамилия' : app.student.last_name,
                'Имя' : app.student.first_name,
                'Отчество' : app.student.middle_name,
                'Параллель' : app.parallel,
                'Класс' : app.group,
                'Дата' : app.stage_subject.date,
            })
        else:
            data['Все'].append({
                'Предмет' : app.stage_subject.subject.name,
                'Фамилия' : app.student.last_name,
                'Имя' : app.student.first_name,
                'Отчество' : app.student.middle_name,
                'Параллель' : app.group,
                'Класс' : app.group,
                'Дата' : app.stage_subject.date,
            })

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f"attachment; filename={translit(stage.name, 'ru', reversed=True)}_participants.xlsx"
    processing.create_excel(data, response)
    
    return response


def application_add(request, olymp_id, stage_id, stage_subject_id):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            try:
                application = form.save(commit=True)

                return HttpResponseRedirect(reverse('olymps:stage_subject_detail', args=(application.stage_subject.stage.olymp.id, application.stage_subject.stage.id, application.stage_subject.id)))
            except ValidationError:
                return HttpResponse("hkbfdavsjdfksl")
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")
    else:
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
        context = {
            'olymp' : olymp,
            'stage' : stage,
            'subject' : subject,
            'form' : ApplicationForm(instance=Application(stage_subject=subject)),
        }
        return render(request, 'olymps/stage/subject/applications/add.html', context)


def application_add_file(request, olymp_id, stage_id, stage_subject_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    if request.method == "POST":
        context = {
            'olymp' : olymp,
            'stage' : stage,
            'subject' : subject,
            'to_add' : [],
            'to_update' : [],
            'no_change' : [],
            'errors' : [],
        }
        try:
            checks = {
                'middle_name' : 'middle_name' in request.POST,
                'group' : 'group' in request.POST,
                'alumnus' : 'alumnus' in request.POST,
            }
            processing.get_applications_update_lists(request, context, subject, checks)
            return render(request, 'olymps/stage/subject/applications/add_file_preview.html', context)
        except:
            return HttpResponse("Произошла ошибка")
    else:
        context = {
            'olymp' : olymp,
            'stage' : stage,
            'subject' : subject,
        }
        return render(request, 'olymps/stage/subject/applications/add_file.html', context)


def application_add_file_submit(request, olymp_id, stage_id, stage_subject_id):
    if request.method == "POST":
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
        try:
            processing.save_applications_update_lists(request, subject)
            return HttpResponseRedirect(reverse('olymps:stage_subject_detail', args=(subject.stage.olymp.id, subject.stage.id, subject.id)))
        except:
            return HttpResponse("Произошла ошибка")
    else:
        return 


def application_edit(request, olymp_id, stage_id, stage_subject_id, app_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    application = get_object_or_404(Application, id=app_id, stage_subject=subject)
    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        application = form.save(commit=False)
        if application.student.group and not application.group:
            application.group = str(application.student.group)
            form.group = str(application.student.group)
        if application.student.group and not application.parallel:
            application.parallel = application.student.group.num
            form.parallel = application.student.group.num
        if not application.student.group and not application.group:
            return HttpResponse("Не указан класс участия")
        if form.is_valid():
            try:
                application.save()
                return HttpResponseRedirect(reverse('olymps:stage_subject_detail', args=(application.stage_subject.stage.olymp.id, application.stage_subject.stage.id, application.stage_subject.id)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Данные некорректны")
    else:
        context = {
            'olymp' : olymp,
            'stage' : stage,
            'subject' : subject,
            'application' : application,
            'form' : ApplicationForm(instance=application),
        }
        return render(request, 'olymps/stage/subject/applications/edit.html', context)

def application_delete(request, olymp_id, stage_id, stage_subject_id, app_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    application = get_object_or_404(Application, stage_subject=subject, id=app_id)
    if request.method == 'POST':
        try:
            application.delete()
            return HttpResponseRedirect(reverse('olymps:stage_subject_detail', args=(olymp_id, stage_id, stage_subject_id)))
        except:
            return HttpResponse('Произошла ошибка')
    else:
        return HttpResponse('Некорректный метод запроса')


def application_mass_edit(request, olymp_id, stage_id, stage_subject_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    if request.method == 'POST':
        formset = ApplicationFormset(request.POST, prefix='app')
        if formset.is_valid():
            try:
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:stage_subject_detail', args=(olymp_id, stage_id, stage_subject_id)))
            except:
                return HttpResponse("Произошла ошибка")
    else:
        context = {
            'subject' : subject,
            'formset' : ApplicationFormset(prefix='app', queryset=subject.application_set.all().order_by('parallel', 'status', '-result', 'group', 'student__last_name', 'student__first_name', 'student__middle_name'))
        }
        return render(request, 'olymps/stage/subject/applications/mass_edit.html', context)

def application_parallel_mass_edit(request, olymp_id, stage_id, stage_subject_id, parallel):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
    
    if not(subject.min_class <= parallel and parallel <= subject.max_class):
        return HttpResponseNotFound()

    if request.method == 'POST':
        formset = ApplicationFormset(request.POST, prefix='app')
        if formset.is_valid():
            try:
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:stage_subject_parallel', args=(olymp_id, stage_id, stage_subject_id, parallel)))
            except:
                return HttpResponse("Произошла ошибка")
    else:
        context = {
            'subject' : subject,
            'parallel' : parallel,
            'formset' : ApplicationFormset(prefix='app', queryset=subject.application_set.filter(parallel=parallel).order_by('student__last_name', 'student__first_name', 'student__middle_name'))
        }
        return render(request, 'olymps/stage/subject/applications/parallel_mass_edit.html', context)

def application_parallel_grade_win_set(request, olymp_id, stage_id, stage_subject_id, parallel):
    if request.method == 'POST':
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
        if not(subject.min_class <= parallel and parallel <= subject.max_class):
            return HttpResponseNotFound()
        grade = get_object_or_404(Grade, stage_subject=subject, parallel=parallel)
        apps = subject.application_set.filter(parallel=parallel).exclude(status=Status.DISQUALIFIED)
        try:
            grade.gold = float(request.POST['grade-gold'])
            grade.silver = float(request.POST['grade-silver'])
            gold = apps.filter(result__gte=grade.gold)
            silver = apps.filter(result__gte=grade.silver, result__lt=grade.gold)
            part = apps.filter(result__lt=grade.silver)
            abcent = apps.filter(result=None)
            grade.save()
            gold.update(status=Status.WINNER)
            silver.update(status=Status.PRIZER)
            part.update(status=Status.PARTICIPANT)
            abcent.update(status=Status.ABSENT)
            return HttpResponseRedirect(reverse('olymps:stage_subject_parallel', args=(olymp_id, stage_id, stage_subject_id, parallel)))
        except:
            return HttpResponse('Произошла ошибка')
    else:
        return HttpResponse('Некорректный метод запроса')

def application_parallel_add_prev_num(request, olymp_id, stage_id, stage_subject_id, parallel):
    if request.method == 'POST':
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
        if not(subject.min_class <= parallel and parallel <= subject.max_class):
            return HttpResponseNotFound()
        grade = get_object_or_404(Grade, stage_subject=subject, parallel=parallel)
        try:
            apps = olymp.olympstage_set.get(num=stage.num - 1).olympstagesubject_set.get(subject=subject.subject).application_set.filter(parallel=parallel).exclude(status=Status.DISQUALIFIED)
            grade.participate = float(request.POST['grade-participate'])
            apps = apps.filter(result__gte=grade.participate)
            for old in apps:
                if subject.application_set.filter(student=old.student).exists():
                    continue
                app = copy(old)
                app.id = None
                app.stage_subject = subject
                app.code = None
                app.result = None
                app.status = None
                app.save()
            grade.save()
            
            return HttpResponseRedirect(reverse('olymps:stage_subject_parallel', args=(olymp_id, stage_id, stage_subject_id, parallel)))
        except:
            return HttpResponse('Произошла ошибка')
    else:
        return HttpResponse('Некорректный метод запроса')


def application_parallel_add_prev_year(request, olymp_id, stage_id, stage_subject_id, parallel):
    if request.method == 'POST':
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        subject = get_object_or_404(OlympStageSubject, stage=stage, id=stage_subject_id)
        if not(subject.min_class <= parallel and parallel <= subject.max_class):
            return HttpResponseNotFound()
        try:
            prevolymp = Olymp.objects.get(name=olymp.name, year=olymp.year - 1)
            apps = prevolymp.olympstage_set.get(num=stage.num).olympstagesubject_set.get(subject=subject.subject).application_set.all()
            apps = apps.filter(Q(status=Status.PRIZER) | Q(status=Status.WINNER))
            for old in apps:
                if subject.application_set.filter(student=old.student).exists():
                    continue
                if Application.objects.filter(stage_subject__stage__olymp=olymp, student=old.student, status=Status.DISQUALIFIED).exists():
                    continue
                app = copy(old)
                if app.student.group:
                    app.parallel = max(subject.min_class, app.student.group.num)
                    app.group = str(app.student.group)
                else:
                    app.parallel = min(max(subject.min_class, app.parallel + 1), subject.max_class)
                    app.group = None
                app.id = None
                app.stage_subject = subject
                app.code = None
                app.result = None
                app.status = None
                if app.parallel == parallel:
                    app.save()
            
            return HttpResponseRedirect(reverse('olymps:stage_subject_parallel', args=(olymp_id, stage_id, stage_subject_id, parallel)))
        except:
            return HttpResponse('Произошла ошибка')
    else:
        return HttpResponse('Некорректный метод запроса')