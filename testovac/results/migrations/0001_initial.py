# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-09 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tasks", "0002_auto_20160709_1055"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomResultsTable",
            fields=[
                (
                    "slug",
                    models.SlugField(
                        help_text=b'Serves as part of URL.<br />Must only contain characters "a-zA-Z0-9_-".',
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("contests", models.ManyToManyField(to="tasks.Contest")),
            ],
            options={
                "verbose_name": "custom results table",
                "verbose_name_plural": "custom results tables",
            },
        ),
    ]
