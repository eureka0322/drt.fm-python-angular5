# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_initial_order(apps, schema_editor):
    model = apps.get_model('post', 'Post')
    for s in model.objects.all():
        s.order = s.pk
        s.save()


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_post_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='post',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.RunPython(
            set_initial_order,
            reverse_code=lambda apps, schema_editor: None
        ),
    ]
