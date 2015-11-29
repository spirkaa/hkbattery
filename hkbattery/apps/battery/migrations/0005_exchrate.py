# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battery', '0004_auto_20151115_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchRate',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('ex_rate', models.DecimalField(verbose_name='EUR to RUB', max_digits=6, decimal_places=2)),
            ],
        ),
    ]
