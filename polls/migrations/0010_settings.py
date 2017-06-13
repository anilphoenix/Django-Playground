# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-09 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_project_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(max_length=1000)),
                ('option_value', models.CharField(max_length=25000)),
                ('option_meta', models.CharField(max_length=1000)),
            ],
        ),
    ]
