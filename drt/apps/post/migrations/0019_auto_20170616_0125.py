# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0018_auto_20170314_0932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='featured',
            new_name='popular',
        ),
    ]
