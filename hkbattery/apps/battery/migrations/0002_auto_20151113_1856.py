# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battery',
            name='cap_to_price',
            field=models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Cap to Price'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='cap_to_weight',
            field=models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Cap to Weight'),
        ),
    ]
