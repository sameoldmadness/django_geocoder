# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geocoder', '0008_auto_20170319_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
