from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from datetime import date
from django.utils import timezone

import pandas as pd

from students.models import Student, Group
from .models import Olymp, OlympStage, OlympStageSubject

def index(request):
    olymps_list = Olymp.objects.all()
    context = {'olymps': olymps_list}
    return render(request, 'olymps/index.html', context)