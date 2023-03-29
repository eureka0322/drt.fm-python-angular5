# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45, verbose_name=b'Name')),
                ('color', models.CharField(max_length=7, verbose_name=b'Color')),
                ('slug', models.CharField(unique=True, max_length=45, verbose_name=b'Slug')),
                ('default', models.BooleanField(default=False, verbose_name=b'Default')),
                ('order', models.IntegerField(default=0, verbose_name=b'Order')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guest', models.CharField(max_length=255, verbose_name=b'Guest Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, unique=True, populate_from=b'guest')),
                ('job', models.CharField(max_length=255, verbose_name=b'Job Title')),
                ('title', models.CharField(max_length=255, verbose_name=b'Interview Title')),
                ('description', models.TextField(default=b'', verbose_name=b'Summary')),
                ('quote', models.TextField(default=b'', verbose_name=b'Quote')),
                ('image', s3direct.fields.S3DirectField(default=b'')),
                ('url', models.CharField(default=b'', max_length=255, verbose_name=b'Audio URL')),
                ('twitter', models.CharField(max_length=255, verbose_name=b'Twitter Handle')),
                ('education', models.CharField(max_length=255, verbose_name=b'Education')),
                ('educationUrl', models.CharField(max_length=255, null=True, verbose_name=b'Education URL', blank=True)),
                ('app', models.CharField(max_length=255, null=True, verbose_name=b'App Name', blank=True)),
                ('appUrl', models.CharField(max_length=255, null=True, verbose_name=b'App URL', blank=True)),
                ('book', models.CharField(max_length=255, null=True, verbose_name=b'Book Title', blank=True)),
                ('bookUrl', models.CharField(max_length=255, null=True, verbose_name=b'Book URL', blank=True)),
                ('roleModel', models.CharField(max_length=255, null=True, verbose_name=b'Role Model', blank=True)),
                ('roleModelUrl', models.CharField(max_length=255, null=True, verbose_name=b'Role Model URL', blank=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name=b'Publish Date', auto_now_add=True)),
                ('category', models.ForeignKey(default=None, to='post.Category')),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
    ]
