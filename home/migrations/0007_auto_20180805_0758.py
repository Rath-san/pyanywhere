# Generated by Django 2.0.8 on 2018-08-05 05:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('home', '0006_auto_20180804_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareerIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='careeritem',
            name='page',
        ),
        migrations.AddField(
            model_name='careerpage',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, verbose_name='Opis stanowiska'),
        ),
        migrations.DeleteModel(
            name='CareerItem',
        ),
    ]