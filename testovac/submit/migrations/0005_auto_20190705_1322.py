# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-07-05 11:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("submit", "0004_submit_is_pulic"),
    ]

    operations = [
        migrations.RenameField(
            model_name="submit",
            old_name="is_pulic",
            new_name="is_public",
        ),
    ]
