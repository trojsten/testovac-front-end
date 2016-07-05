# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
        ('tasks', '0002_task_submit_receiver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='submit_receiver',
        ),
        migrations.AddField(
            model_name='task',
            name='submit_receiver',
            field=models.ManyToManyField(to='submit.SubmitReceiver'),
        ),
    ]