# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PodcastFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='Dorm Room Tycoon - Business, Design &amp; Technology Interviews', max_length=255, verbose_name=b'Title')),
                ('description', models.TextField(default='The podcast show that interviews the biggest names in business, design and tech.', verbose_name=b'Description')),
                ('image', s3direct.fields.S3DirectField(default='', verbose_name=b'Image URL')),
                ('subtitle', models.TextField(default="Insightful interviews for hackers, product designers and startup founders. Learning from the world's most influential creators!", verbose_name=b'iTunes Subtitle')),
                ('author', models.CharField(default='William Channer', max_length=255, verbose_name=b'iTunes Owner Name')),
                ('email', models.CharField(default='william.channer@gmail.com', max_length=255, verbose_name=b'iTunes Owner Email')),
                ('explicit', models.BooleanField(default=True, max_length=1, verbose_name=b'iTunes Explicit', choices=[(False, 'No'), (True, 'Yes')])),
                ('summary', models.TextField(default='Interviews for designers, hackers, and startup founders.', verbose_name=b'iTunes Summary')),
                ('keywords', models.TextField(default='drt, design, marketing, business, entrepreneurship, silicon valley, kickstarter, product, innovation, startup, product hunt', verbose_name=b'iTunes Keywords')),
                ('copyright', models.CharField(default='Copyright %s Dorm Room Tycoon', max_length=255, verbose_name=b'Copyright')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
