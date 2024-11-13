import django.forms as forms
from django.core.exceptions import ValidationError

from olymps.models import *


class OlympForm(forms.ModelForm):
    class Meta:
        model = Olymp
        fields = ['name', 'year']


class BaseStageFormSet(forms.BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        nums = set()
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            num = form.cleaned_data.get("num")
            if not num:
                raise ValidationError("Оставлен пустой номер этапа")
            if num in nums:
                raise ValidationError("Все номера этапов должны быть разными")
            nums.add(num)

OlympStageFormset = forms.modelformset_factory(OlympStage, fields=['id', 'num'], extra=0, formset=BaseStageFormSet)