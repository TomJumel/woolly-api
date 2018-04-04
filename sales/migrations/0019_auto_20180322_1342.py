# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-22 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_auto_20170616_1450'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='itemspecifications',
        #     name='fun_id',
        #     field=models.CharField(default='', max_length=30),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='order',
        #     name='hash_key',
        #     field=models.CharField(default='', max_length=50),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='order',
        #     name='price',
        #     field=models.FloatField(default=0),
        #     preserve_default=False,
        # ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='begin_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='max_payment_date',
            field=models.DateTimeField(),
        ),
    ]