from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from datetime import date
from django.utils import timezone

import pandas as pd

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
        # try:
        f = request.FILES['file']
        processing.stages_file(f, olymp)
        return HttpResponseRedirect(reverse('olymps:detail', args=(olymp.id,)))
        # except:
        #     return HttpResponse("Произошла ошибка")
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
    applications = Application.objects.filter(stage_subject=subject).order_by('student')
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
    applications = Application.objects.filter(stage_subject=subject, parallel=parallel).order_by('status', '-result')
    context = {
        'subject' : subject,
        'applications' : applications,
        'parallels' : list(range(subject.min_class, subject.max_class + 1)) if subject.min_class <= subject.max_class else None,
        'parallel' : parallel,
    }
    return render(request, 'olymps/stage/subject/parallel.html', context)

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
            processing.save_students_update_lists(request)
            return HttpResponseRedirect(reverse('olymp: '))
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
