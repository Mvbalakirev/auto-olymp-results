# Generated by Django 5.1.3 on 2024-11-29 00:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olymps', '0008_alter_olympstagesubject_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='olympstagesubject',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olymps.olympstage', verbose_name='Этап'),
        ),
    ]