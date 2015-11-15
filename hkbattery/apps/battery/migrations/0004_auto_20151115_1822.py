# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battery', '0003_auto_20151115_1819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='battery',
            options={'verbose_name_plural': 'Batteries', 'ordering': ['s_config'], 'verbose_name': 'Battery'},
        ),
        migrations.AlterField(
            model_name='battery',
            name='amps',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Current, A'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='cap_to_price',
            field=models.DecimalField(max_digits=6, blank=True, null=True, verbose_name='Cap / price', decimal_places=2),
        ),
        migrations.AlterField(
            model_name='battery',
            name='cap_to_weight',
            field=models.DecimalField(max_digits=6, blank=True, null=True, verbose_name='Cap / weight', decimal_places=2),
        ),
        migrations.AlterField(
            model_name='battery',
            name='capacity',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Capacity, mAh'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='charge',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Charge, C'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='discharge',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Discharge, C'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='height',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Height, mm'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='length',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Length, mm'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='price',
            field=models.DecimalField(max_digits=6, verbose_name='Price, €', decimal_places=2),
        ),
        migrations.AlterField(
            model_name='battery',
            name='s_config',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Config, S'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='weight',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Weight, g'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='width',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Width, mm'),
        ),
    ]
