# Generated by Django 5.1.3 on 2024-12-04 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olymps', '0011_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='result',
            field=models.FloatField(blank=True, null=True, verbose_name='Баллы'),
        ),
    ]
