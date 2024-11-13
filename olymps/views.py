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
    stages = OlympStage.objects.filter(olymp=olymp).order_by('num')
    context = {
        'olymp' : olymp,
        'stages' : stages
    }
    return render(request, 'olymps/detail.html', context)

def edit(request, olymp_id):
    olymp = get_object_or_404(Olymp, pk=olymp_id)
    stages = OlympStage.objects.filter(olymp=olymp).order_by('num')
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
            form.save(commit=True)
            formset.save(commit=True)

            return HttpResponseRedirect(reverse('olymps:detail', args=(olymp_id,)))
        else:
            return HttpResponse("Произошла ошибка")

    return render(request, 'olymps/edit.html', context)

def stage_add(request, stage_id):
    return HttpResponse('')

def stage_delete(request, stage_id):
    if request.method == 'POST':
        pass
    else:
        return HttpResponse('Некорректный метод запроса')