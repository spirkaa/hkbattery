import logging
from collections import OrderedDict
from decimal import Decimal
from django.db import models
from django.db.models import Avg, Count, F, Max, Min, Sum, Q, Prefetch, Case, When
from django_extensions.db.models import TimeStampedModel
from .decorators import async
from .battery_parser import parser

logger = logging.getLogger(__name__)


class CommonInfo(TimeStampedModel):
    link = models.URLField('Link to HobbyKing', unique=True)
    name = models.CharField('Name', max_length=200)
    pic = models.URLField('Image link', blank=True)
    price = models.DecimalField('Price, €', max_digits=6, decimal_places=2)
    ru_stock = models.SmallIntegerField('RU stock', null=True, blank=True)

    class Meta:
        abstract = True


class Battery(CommonInfo):
    s_config = models.SmallIntegerField('Config, S', null=True, blank=True)
    capacity = models.SmallIntegerField('Capacity, mAh', null=True, blank=True)
    weight = models.SmallIntegerField('Weight, g', null=True, blank=True)
    cap_to_weight = models.DecimalField('Cap / weight', null=True, blank=True, max_digits=6, decimal_places=2)
    cap_to_price = models.DecimalField('Cap / price', null=True, blank=True, max_digits=6, decimal_places=2)
    discharge = models.SmallIntegerField('Discharge, C', null=True, blank=True)
    amps = models.SmallIntegerField('Current, A', null=True, blank=True)
    charge = models.SmallIntegerField('Charge, C', null=True, blank=True)
    length = models.SmallIntegerField('Length, mm', null=True, blank=True)
    height = models.SmallIntegerField('Height, mm', null=True, blank=True)
    width = models.SmallIntegerField('Width, mm', null=True, blank=True)

    class Meta:
        verbose_name = 'Battery'
        verbose_name_plural = 'Batteries'
        ordering = ['s_config']

    @property
    def price_rub(self):
        return self.price * 72

    def __str__(self):
        return self.name


def min_max_values():
    field_list = ['price', 'ru_stock', 's_config',
                  'capacity', 'discharge', 'weight']
    min_max_list = []
    q = Battery.objects.all()
    for name in field_list:
        verb_name = Battery._meta.get_field(name).verbose_name.title()
        v_name = {'v_name': verb_name}
        min_val = q.aggregate(Min(name))
        min_val['min'] = min_val.pop('%s__min' % name)
        max_val = q.aggregate(Max(name))
        max_val['max'] = max_val.pop('%s__max' % name)
        valdict = {**v_name, **{**min_val, **max_val}}
        min_max_list.append(valdict)
    return OrderedDict(zip(field_list, min_max_list))


def db_operations(results, operation):
    for r in results:
        try:
            amps_c = round((float(r['capacity'])/1000 * float(r['discharge'])), 2)
            ctp = round((float(r['capacity']) / float(r['price'])), 2)
            ctw = round((float(r['capacity']) / float(r['weight'])), 2)
        except:
            pass
        if operation == 'populate':
            try:
                logger.info('Insert "%s"' % r['name'])
                item = Battery(amps=amps_c,
                               cap_to_price=ctp,
                               cap_to_weight=ctw,
                               **r)
                item.save()
            except:
                logger.error('Cant insert %s, skip' % r['name'])
                raise
        elif operation == 'update':
            r['amps'] = amps_c
            r['cap_to_price'] = ctp
            r['cap_to_weight'] = ctw
            item, created = Battery.objects.get_or_create(link=r['link'],
                                                          defaults=r)
            if item.price != Decimal(r['price']):
                item.price = r['price']
                item.save()
                logger.info('Updade "%s" PRICE', item.name)
            if item.ru_stock != int(r['ru_stock']):
                item.ru_stock = r['ru_stock']
                logger.info('Updade "%s" STOCK', item.name)
                item.save()


@async
def run_db_operation(operation):
    results = parser()
    db_operations(results, operation)
