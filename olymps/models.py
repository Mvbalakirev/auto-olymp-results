import datetime

from django.db import models
from django.utils import timezone

import students.models
from django.utils.translation import gettext_lazy as _

class Subject(models.Model):
    name = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

class Olymp(models.Model):
    name = models.CharField('Название', max_length=255)
    year = models.IntegerField('Год', help_text="Укажите первый год учебного года")

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

class OlympStageSubject(models.Model):
    stage = models.ForeignKey(OlympStage, on_delete=models.CASCADE, verbose_name='Этап')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='Предмет')
    min_class = models.IntegerField('Минимальный класс')
    max_class = models.IntegerField('Максимальный класс')
    date = models.DateField('Дата проведения', null=True, blank=True)

    def __str__(self):
        return str(self.stage) + ' | ' + self.subject.name
    
    class Meta:
        verbose_name = 'предмет этапа'
        verbose_name_plural = 'предметы этапа'
        unique_together = ('stage', 'subject')

class Grade(models.Model):
    stage_subject = models.ForeignKey(OlympStageSubject, on_delete=models.CASCADE, verbose_name='Предмет')
    group_num = models.IntegerField('Класс')
    gold = models.FloatField('Победитель', null=True, blank=True)
    silver = models.FloatField('Призёр', null=True, blank=True)
    participate = models.FloatField('Проходной балл', null=True, blank=True)

    class Meta:
        verbose_name = 'пороговые баллы'
        verbose_name_plural = 'пороговые баллы'



class Status(models.IntegerChoices):
        WINNER = 1, _('Победитель')
        PRIZER = 2, _('Призёр')
        PARTICIPANT = 3, _('Участник')
        DISQUALIFIED = 100, _('Дискв.')
        ABSENT = 200, _('Неявка')
        __empty__ = _('')

class Application(models.Model):
    stage_subject = models.ForeignKey(OlympStageSubject, on_delete=models.PROTECT, verbose_name='Предмет этапа')
    student = models.ForeignKey(students.models.Student, on_delete=models.PROTECT, verbose_name='Участник')
    group = models.CharField('Класс', max_length=255, null=True, blank=True)
    parallel = models.IntegerField('Класс участия')
    code = models.CharField('Код', max_length=255, null=True, blank=True)
    result = models.FloatField('Баллы', null=True, blank=True)
    status = models.IntegerField('Статус', choices=Status, null=True, blank=True)

    def __str__(self):
        return str(self.student.fio()) + " — " + str(self.stage_subject)

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'
        unique_together = ('stage_subject', 'student')