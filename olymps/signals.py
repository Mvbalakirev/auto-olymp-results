from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from students.models import *

@receiver(post_save, sender=OlympStageSubject)
def update_grades(sender, instance, created, **kwargs):
    instance.grade_set.exclude(parallel__lte=instance.max_class, parallel__gte=instance.min_class).delete()
    for paral in range(instance.min_class, instance.max_class + 1) if instance.min_class <= instance.max_class else []:
        instance.grade_set.get_or_create(parallel=paral)
