# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151214_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillvalue',
            name='value',
            field=models.FloatField(),
        ),
    ]