# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_remove_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='foundation_id',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemspecifications',
            name='nemopay_id',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]