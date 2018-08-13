# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-09 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('home', '0018_offercategorypage_intro_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerindexpage',
            name='intro_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
