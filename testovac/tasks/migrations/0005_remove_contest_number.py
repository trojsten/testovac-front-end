# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-10 13:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0004_competition_contests"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contest",
            name="number",
        ),
    ]
