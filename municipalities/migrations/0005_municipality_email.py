# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipalities', '0004_auto_20160505_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipality',
            name='email',
            field=models.TextField(null=True),
        ),
    ]
