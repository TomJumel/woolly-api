# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 10:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_associationmember_association'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associationmember',
            name='user',
        ),
        migrations.DeleteModel(
            name='AssociationMember',
        ),
    ]