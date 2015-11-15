import django_tables2 as tables
from .models import Battery


class BatteryTable(tables.Table):
    name = tables.TemplateColumn('<a href="{{record.link}}" target="_blank">{{record.name}}</a>')
    pic = tables.TemplateColumn('<img src="{{record.pic}}" style="width:50px;"/>', orderable=False)
    price_rub = tables.Column(order_by=('price'))

    class Meta:
        model = Battery
        sequence = ('pic', 'name', 'price_rub', 'price', 'ru_stock',
                    's_config', 'capacity', 'weight', 'cap_to_price',
                    'cap_to_weight', 'discharge', 'amps', '...')
        exclude = ('id', 'created', 'modified', 'link')
