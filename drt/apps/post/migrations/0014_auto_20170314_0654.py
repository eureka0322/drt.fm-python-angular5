# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20161108_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='about',
            field=models.TextField(default=b'', null=True, verbose_name=b'About', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='audio_length',
            field=models.IntegerField(default=0, null=True, verbose_name=b'Length in bytes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=None, blank=True, to='post.Category', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(default=b'', null=True, verbose_name=b'Summary', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='duration',
            field=models.CharField(default=b'00:00:00', max_length=8, null=True, verbose_name=b'Duration hh:mm:ss', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='education',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Education', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=s3direct.fields.S3DirectField(default=b'', null=True, verbose_name=b'Image', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='job',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Company Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='quote',
            field=models.TextField(default=b'', null=True, verbose_name=b'Quote', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Interview Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='twitter',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Twitter Handle', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='url',
            field=s3direct.fields.S3DirectField(default=b'', null=True, verbose_name=b'Audio', blank=True),
            preserve_default=True,
        ),
    ]
