# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 14:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=products.models.upload_csv_file)),
                ('date', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('price', models.FloatField(default=0)),
                ('old_price', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=3)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('upc', models.CharField(blank=True, max_length=150)),
                ('ean', models.CharField(blank=True, max_length=13)),
                ('image', models.URLField(blank=True)),
                ('shipping_cost', models.CharField(blank=True, max_length=150)),
                ('stock', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('logo', models.URLField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Shop'),
        ),
        migrations.AddField(
            model_name='csvupload',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Shop'),
        ),
        migrations.AddField(
            model_name='csvupload',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
