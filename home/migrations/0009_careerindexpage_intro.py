# Generated by Django 2.0.8 on 2018-08-05 08:09

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_policy'),
    ]

    operations = [
        migrations.AddField(
            model_name='careerindexpage',
            name='intro',
            field=wagtail.core.fields.RichTextField(blank=True, verbose_name='intro dla indeksu karier'),
        ),
    ]
