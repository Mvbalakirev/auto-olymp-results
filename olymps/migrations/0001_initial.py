# Generated by Django 5.1.3 on 2024-12-16 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Olymp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('year', models.IntegerField(help_text='Укажите первый год учебного года', verbose_name='Год')),
            ],
            options={
                'verbose_name': 'олимпиада',
                'verbose_name_plural': 'олимпиады',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'предмет',
                'verbose_name_plural': 'предметы',
            },
        ),
        migrations.CreateModel(
            name='OlympStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('num', models.IntegerField(verbose_name='Порядковый номер')),
                ('olymp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='olymps.olymp', verbose_name='Олимпиада')),
            ],
            options={
                'verbose_name': 'этап',
                'verbose_name_plural': 'этапы',
            },
        ),
        migrations.CreateModel(
            name='OlympStageSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_class', models.IntegerField(verbose_name='Минимальный класс')),
                ('max_class', models.IntegerField(verbose_name='Максимальный класс')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата проведения')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olymps.olympstage', verbose_name='Этап')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='olymps.subject', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'предмет этапа',
                'verbose_name_plural': 'предметы этапа',
                'unique_together': {('stage', 'subject')},
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parallel', models.IntegerField(verbose_name='Класс')),
                ('gold', models.FloatField(blank=True, null=True, verbose_name='Победитель')),
                ('silver', models.FloatField(blank=True, null=True, verbose_name='Призёр')),
                ('participate', models.FloatField(blank=True, null=True, verbose_name='Проходной балл')),
                ('stage_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olymps.olympstagesubject', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'пороговые баллы',
                'verbose_name_plural': 'пороговые баллы',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, max_length=255, null=True, verbose_name='Класс')),
                ('parallel', models.IntegerField(verbose_name='Класс участия')),
                ('code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Код')),
                ('result', models.FloatField(blank=True, null=True, verbose_name='Баллы')),
                ('status', models.IntegerField(blank=True, choices=[(None, ''), (1, 'Победитель'), (2, 'Призёр'), (3, 'Участник'), (100, 'Дискв.'), (200, 'Неявка')], null=True, verbose_name='Статус')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='students.student', verbose_name='Участник')),
                ('stage_subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='olymps.olympstagesubject', verbose_name='Предмет этапа')),
            ],
            options={
                'verbose_name': 'заявка',
                'verbose_name_plural': 'заявки',
                'unique_together': {('stage_subject', 'student')},
            },
        ),
    ]
