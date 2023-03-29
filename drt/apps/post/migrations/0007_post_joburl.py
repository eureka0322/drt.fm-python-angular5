# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20161020_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='jobUrl',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Job URL', blank=True),
            preserve_default=True,
        ),
    ]
