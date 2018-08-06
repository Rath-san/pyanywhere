# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-04 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_offerindexpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerindexpage',
            name='body',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='offerindexpage',
            name='intro',
            field=models.CharField(max_length=250),
        ),
    ]
