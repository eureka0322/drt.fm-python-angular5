# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_post_joburl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=s3direct.fields.S3DirectField(default=b'', verbose_name=b'Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='url',
            field=s3direct.fields.S3DirectField(default=b'', verbose_name=b'Audio'),
            preserve_default=True,
        ),
    ]
