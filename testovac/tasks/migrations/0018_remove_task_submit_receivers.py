# Generated by Django 2.2.15 on 2020-08-08 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0017_task_show_details"),
        ("submit", "0007_auto_20200808_1532"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="submit_receivers",
        ),
    ]
