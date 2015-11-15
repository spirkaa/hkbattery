# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Battery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True)),
                ('link', models.URLField(unique=True, verbose_name='Link to HobbyKing')),
                ('name', models.CharField(verbose_name='Name', max_length=200)),
                ('pic', models.URLField(blank=True, verbose_name='Image link')),
                ('price', models.DecimalField(verbose_name='Price (euro)', max_digits=6, decimal_places=2)),
                ('ru_stock', models.SmallIntegerField(blank=True, verbose_name='RU stock', null=True)),
                ('s_config', models.SmallIntegerField(blank=True, verbose_name='Config (S)', null=True)),
                ('capacity', models.SmallIntegerField(blank=True, verbose_name='Capacity (mAh)', null=True)),
                ('weight', models.SmallIntegerField(blank=True, verbose_name='Weight (g)', null=True)),
                ('cap_to_weight', models.SmallIntegerField(blank=True, verbose_name='Cap to Weight', null=True)),
                ('cap_to_price', models.SmallIntegerField(blank=True, verbose_name='Cap to Price', null=True)),
                ('discharge', models.SmallIntegerField(blank=True, verbose_name='Discharge (C)', null=True)),
                ('amps', models.SmallIntegerField(blank=True, verbose_name='Current (A)', null=True)),
                ('charge', models.SmallIntegerField(blank=True, verbose_name='Charge (C)', null=True)),
                ('length', models.SmallIntegerField(blank=True, verbose_name='Length-A (mm)', null=True)),
                ('height', models.SmallIntegerField(blank=True, verbose_name='Height-B (mm)', null=True)),
                ('width', models.SmallIntegerField(blank=True, verbose_name='Width-C (mm)', null=True)),
            ],
            options={
                'verbose_name': 'Battery',
                'verbose_name_plural': 'Batteries',
                'ordering': ['price'],
            },
        ),
    ]
