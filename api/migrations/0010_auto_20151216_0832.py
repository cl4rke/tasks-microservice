# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 00:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20151215_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='estimated_time',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_completed',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
