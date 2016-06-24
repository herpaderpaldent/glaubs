# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-24 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipalities', '0006_municipality_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipality',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='email',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='phone_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='website',
            field=models.TextField(blank=True, null=True),
        ),
    ]
