# Generated by Django 5.1.3 on 2024-11-08 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_alter_student_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
