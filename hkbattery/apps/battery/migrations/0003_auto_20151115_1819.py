# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battery', '0002_auto_20151113_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battery',
            name='height',
            field=models.SmallIntegerField(null=True, verbose_name='Height (mm)', blank=True),
        ),
        migrations.AlterField(
            model_name='battery',
            name='length',
            field=models.SmallIntegerField(null=True, verbose_name='Length (mm)', blank=True),
        ),
        migrations.AlterField(
            model_name='battery',
            name='width',
            field=models.SmallIntegerField(null=True, verbose_name='Width (mm)', blank=True),
        ),
    ]
