# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-04 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20180804_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='footer_copyright',
            field=models.CharField(blank='true', max_length=255),
        ),
    ]
