from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from datetime import date
from django.utils import timezone

import pandas as pd

from students.models import Student, Group
from .models import Olymp, OlympStage, OlympStageSubject
from .forms import *

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
                form.save(commit=True)
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:detail', args=(olymp_id,)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Произошла ошибка")

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
            return HttpResponse("Произошла ошибка")
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
            return HttpResponse("Произошла ошибка")
    else:
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        context = {
            'olymp' : olymp,
            'form' : StageForm(instance=OlympStage(olymp=olymp)),
        }
        return render(request, 'olymps/stage/add.html', context)

def stage_detail(request, olymp_id, stage_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subjects = stage.olympstagesubject_set.all().order_by('date')
    context = {
        'stage' : stage,
        'stage_subjects' : subjects
    }
    return render(request, 'olymps/stage/detail.html', context)

def stage_edit(request, olymp_id, stage_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
    subjects = stage.olympstagesubject_set.all().order_by('date')
    
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
                form.save(commit=True)
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('olymps:stage_detail', args=(olymp_id, stage_id,)))
            except:
                return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Произошла ошибка")

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
            # try:
            stage_subject = form.save(commit=True)
            return HttpResponseRedirect(reverse('olymps:stage_detail', args=(stage_subject.stage.olymp.id, stage_subject.stage.id)))
            # except:
            return HttpResponse("Произошла ошибка")
        else:
            return HttpResponse("Произошла ошибка")
    else:
        olymp = get_object_or_404(Olymp, pk=olymp_id)
        stage = get_object_or_404(OlympStage, olymp=olymp, id=stage_id)
        context = {
            'olymp' : olymp,
            'stage' : stage,
            'form' : StageSubjectForm(instance=OlympStageSubject(stage=stage)),
        }
        return render(request, 'olymps/stage/subject/add.html', context)