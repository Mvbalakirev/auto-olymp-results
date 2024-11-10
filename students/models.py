import datetime

from django.db import models
from django.utils import timezone


class Group(models.Model):
    num = models.IntegerField()
    liter = models.CharField(max_length=2)
    alumnus = models.BooleanField(default=False)

    class Meta:
        unique_together = ('num', 'liter')

    def __str__(self):
        return str(self.num) + ' ' + self.liter


class Student(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return self.last_name + ' ' + self.first_name + \
            (' ' + self.middle_name if self.middle_name else '') + \
            (' ' + str(self.group) if self.group else '')
