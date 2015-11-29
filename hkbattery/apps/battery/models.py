import logging
from decimal import Decimal
from django.db import models
from django.db.models import Max, Min
from django_extensions.db.models import TimeStampedModel
from .decorators import async
from .battery_parser import parser

logger = logging.getLogger(__name__)


class ExchRate(models.Model):
    ex_rate = models.DecimalField('EUR to RUB', max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.ex_rate)

ex_rate = ExchRate.objects.get(pk=1).ex_rate


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
    cap_to_weight = models.DecimalField('Cap / weight', null=True, blank=True,
                                        max_digits=6, decimal_places=2)
    cap_to_price = models.DecimalField('Cap / price', null=True, blank=True,
                                       max_digits=6, decimal_places=2)
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
        # return round((float(self.price) * ex_rate), 2)
        return round((self.price * ex_rate), 2)

    def __str__(self):
        return self.name


def min_max_values():
    fields = ['price', 'ru_stock', 's_config',
              'capacity', 'discharge', 'amps', 'weight']
    min_max = []
    q = Battery.objects.all()
    for field in fields:
        min_val = q.aggregate(Min(field))
        min_val['min'] = min_val.pop('{}__min'.format(field))
        max_val = q.aggregate(Max(field))
        max_val['max'] = max_val.pop('{}__max'.format(field))
        vals_dict = {**min_val, **max_val}
        min_max.append(vals_dict)
    return dict(zip(fields, min_max))


def db_operations(results, operation):
    for r in results:
        try:
            amps_c = round((float(r['capacity'])/1000 * float(r['discharge'])), 2)
            ctp = round((float(r['capacity']) / float(r['price'])), 2)
            ctw = round((float(r['capacity']) / float(r['weight'])), 2)
            r['amps'] = amps_c
            r['cap_to_price'] = ctp
            r['cap_to_weight'] = ctw
        except KeyError:
            pass
        if operation == 'populate':
            try:
                logger.info('Insert "%s"', r['name'])
                item = Battery(**r)
                item.save()
            except:
                logger.error('Cant insert %s, skip', r['name'])
                raise
        elif operation == 'update':
            item, created = Battery.objects.get_or_create(link=r['link'],
                                                          defaults=r)
            # logger.info('%s, %s', item.name, r['price'])
            if item.price != Decimal(r['price']):
                pricelog = item.price
                item.price = r['price']
                try:
                    item.cap_to_price = r['cap_to_price']
                except KeyError:
                    logger.error('"%s" not a battery', item.name)
                item.save()
                logger.info('"%s" PRICE: %s -> %s',
                            item.name, str(pricelog), str(item.price))
            if item.ru_stock != int(r['ru_stock']):
                stocklog = item.ru_stock
                item.ru_stock = r['ru_stock']
                logger.info('"%s" STOCK: %s -> %s',
                            item.name, str(stocklog), str(item.ru_stock))
                item.save()


@async
def run_db_operation(operation):
    results = parser()
    db_operations(results, operation)
