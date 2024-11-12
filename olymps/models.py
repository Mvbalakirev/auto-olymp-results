import datetime

from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

class Olymp(models.Model):
    name = models.CharField('Название', max_length=255)
    year = models.IntegerField('Год')

    def __str__(self):
        return self.name + ' ' + str(self.year) + '/' + str(self.year + 1)
    
    class Meta:
        verbose_name = 'олимпиада'
        verbose_name_plural = 'олимпиады'

class OlympStage(models.Model):
    name = models.CharField('Название', max_length=255)
    olymp = models.ForeignKey(Olymp, on_delete=models.PROTECT, verbose_name='Олимпиада')
    num = models.IntegerField('Порядковый номер')

    def __str__(self):
        return self.name + ' ' + str(self.olymp.year) + '/' + str(self.olymp.year + 1)
    
    class Meta:
        verbose_name = 'этап'
        verbose_name_plural = 'этапы'
        unique_together = ('olymp', 'num')

class OlympStageSubject(models.Model):
    olymp_stage = models.ForeignKey(OlympStage, on_delete=models.PROTECT, verbose_name='Этап')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='Предмет')
    date = models.DateField('Дата проведения', null=True, blank=True)
    min_class = models.IntegerField('Минимальный класс')
    max_class = models.IntegerField('Максимальный класс')

    def __str__(self):
        return self.subject.name
    
    class Meta:
        verbose_name = 'предмет этапа'
        verbose_name_plural = 'предметы этапа'
        unique_together = ('olymp_stage', 'subject')
