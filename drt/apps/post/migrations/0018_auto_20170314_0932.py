# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_auto_20170314_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=45, verbose_name=b'Name')),
                ('text', models.TextField(default=b'', verbose_name=b'Text')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='sponsor',
            field=models.ForeignKey(blank=True, to='post.Sponsorship', null=True),
            preserve_default=True,
        ),
    ]
