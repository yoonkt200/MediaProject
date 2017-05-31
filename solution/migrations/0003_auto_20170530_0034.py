# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solution', '0002_commerce_buyers'),
    ]

    operations = [
        migrations.AddField(
            model_name='commerce',
            name='content',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='commerce',
            name='distance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='commerce',
            name='timer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='commerce',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]