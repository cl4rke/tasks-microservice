# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 01:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_apikey_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='last_login',
            field=models.DateTimeField(),
        ),
    ]
