import django.forms as forms
import formset.widgets
from django.core.exceptions import ValidationError

from .models import *


class OlympForm(forms.ModelForm):
    class Meta:
        model = Olymp
        fields = ['name', 'year']


OlympStageFormset = forms.modelformset_factory(OlympStage, fields=['id', 'num'], extra=0, can_delete=False)


class StageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['olymp'].widget.attrs.update({
            'class' : 'js-chosen'
        })
    
    class Meta:
        model = OlympStage
        fields = ['olymp', 'name', 'num']

class StageSubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = formset.widgets.DateInput()
        self.fields['subject'].widget.attrs.update({
            'class' : 'js-chosen'
        })
        self.fields['stage'].widget.attrs.update({
            'class' : 'js-chosen'
        })

    class Meta:
        model = OlympStageSubject
        fields=['id', 'stage', 'subject', 'min_class', 'max_class', 'date']


StageSubjectsFormset = forms.modelformset_factory(
    OlympStageSubject,
    StageSubjectForm,
    fields=['id', 'min_class', 'max_class', 'date'],
    extra=0,
    can_delete=False
)

class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({
            'class' : 'js-chosen'
        })
        self.fields['stage_subject'].widget.attrs.update({
            'class' : 'js-chosen'
        })
        self.fields['parallel'].required = False
    class Meta:
        model = Application
        fields = ['id', 'stage_subject', 'student', 'group', 'parallel', 'code', 'result', 'status']
