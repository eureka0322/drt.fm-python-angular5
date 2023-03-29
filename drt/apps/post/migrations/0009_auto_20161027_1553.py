# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20161022_0607'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured',
            field=models.BooleanField(default=False, verbose_name=b'Popular'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='job',
            field=models.CharField(max_length=255, verbose_name=b'Company Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='jobUrl',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Company URL', blank=True),
            preserve_default=True,
        ),
    ]
