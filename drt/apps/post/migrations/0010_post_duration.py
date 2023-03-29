# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20161027_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='duration',
            field=models.DecimalField(default=0, verbose_name=b'Audio duration', max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
    ]
