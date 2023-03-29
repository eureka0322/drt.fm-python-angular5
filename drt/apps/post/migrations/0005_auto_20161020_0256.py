# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20161020_0249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='bloUrl',
            new_name='blogUrl',
        ),
    ]
