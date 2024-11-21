import django.forms as forms
import formset.widgets
from django.core.exceptions import ValidationError

from olymps.models import *


class OlympForm(forms.ModelForm):
    class Meta:
        model = Olymp
        fields = ['name', 'year']


OlympStageFormset = forms.modelformset_factory(OlympStage, fields=['id', 'num'], extra=0, can_delete=False)


class StageForm(forms.ModelForm):
    class Meta:
        model = OlympStage
        fields = ['olymp', 'name', 'num']

class StageSubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget = formset.widgets.DateInput()
    class Meta:
        model = OlympStageSubject
        fields=['stage', 'subject', 'min_class', 'max_class', 'date']


StageSubjectsFormset = forms.modelformset_factory(
    OlympStageSubject,
    StageSubjectForm,
    fields=['id', 'min_class', 'max_class', 'date'],
    extra=0,
    can_delete=False
)