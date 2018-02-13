# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-03 21:04
from __future__ import unicode_literals

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20171003_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]