# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 12:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_merge_20170601_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='woollyuser',
            name='type',
        ),
        migrations.DeleteModel(
            name='WoollyUser',
        ),
    ]