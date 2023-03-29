# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_auto_20161101_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='audio_length',
            field=models.IntegerField(default=0, verbose_name=b'Length in bytes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='duration',
            field=models.CharField(default=b'00:00:00', max_length=8, verbose_name=b'Duration hh:mm:ss'),
            preserve_default=True,
        ),
    ]
