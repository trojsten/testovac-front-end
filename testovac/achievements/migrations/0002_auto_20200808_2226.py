# Generated by Django 2.2.15 on 2020-08-08 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("achievements", "0001_squashed_0002_auto_20190705_1509"),
    ]

    operations = [
        migrations.RenameField(
            model_name="achievement",
            old_name="user",
            new_name="users",
        ),
    ]