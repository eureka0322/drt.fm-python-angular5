# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='about',
            field=models.TextField(default=b'', verbose_name=b'About'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='bloUrl',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Blog URL', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='blog',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Blog', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Location', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='locationUrl',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Location URL', blank=True),
            preserve_default=True,
        ),
    ]
