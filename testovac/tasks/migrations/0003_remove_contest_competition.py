# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-10 13:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20160709_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='competition',
        ),
    ]
