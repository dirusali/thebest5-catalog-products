# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-28 02:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20180217_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffilliationNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='automaticproductupdate',
            options={'verbose_name': 'Products Feed', 'verbose_name_plural': 'Product feed list'},
        ),
        migrations.AddField(
            model_name='automaticproductupdate',
            name='advertiser_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='automaticproductupdate',
            name='advertiser_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='automaticproductupdate',
            name='feed_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='automaticproductupdate',
            name='last_imported',
            field=models.DateField(blank=True, help_text='fecha de actualizacion del catalogo en la red', null=True),
        ),
        migrations.AlterField(
            model_name='automaticproductupdate',
            name='last_update',
            field=models.DateTimeField(blank=True, help_text='fecha de actualizacion del catalogo', null=True),
        ),
        migrations.AddField(
            model_name='automaticproductupdate',
            name='affilliation_network',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.AffilliationNetwork'),
        ),
    ]