# Generated by Django 5.1.3 on 2024-12-11 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olymps', '0014_alter_application_status'),
        ('students', '0006_alter_student_group'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('stage_subject', 'student')},
        ),
    ]