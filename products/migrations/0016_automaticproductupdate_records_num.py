# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-06 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_remove_automaticproductupdate_last_import_cmd'),
    ]

    operations = [
        migrations.AddField(
            model_name='automaticproductupdate',
            name='records_num',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]