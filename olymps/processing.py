from datetime import date
from django.utils import timezone
from django.db.models import Max

import pandas as pd

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
            mxnum = OlympStage.objects.filter(olymp=olymp).aggregate(Max('num'))['num__max']
            stage = OlympStage(olymp=olymp, name=stage_name, num=mxnum + 1)
            stage.save()
        for index, row in data.iterrows():
            subject = Subject.objects.get(name=row['subject'])
            try:
                stage_subject = OlympStageSubject.objects.get(stage=stage, subject=subject)
            except:
                stage_subject = OlympStageSubject(stage=stage, subject=subject)
            stage_subject.min_class = row['min_class']
            stage_subject.max_class = row['max_class']
            if row['date'] != '' and row['date'].lower() != 'nan' and row['date'].lower() != 'nat':
                stage_subject.date = row['date']
            else:
                stage_subject.date = None
            stage_subject.save()
