import django_tables2 as tables
from .models import Battery


class BatteryTable(tables.Table):
    name = tables.TemplateColumn(
        '<a href="{{record.link}}" target="_blank">{{record.name}}</a>')
    pic = tables.TemplateColumn(
        '<img src="{{record.pic}}" style="width:50px;"/>', orderable=False)
    price_rub = tables.Column(order_by=('price'))
    cap_to_price = tables.Column(attrs={"td": {"class": "tdbold"}})
    cap_to_weight = tables.Column(attrs={"td": {"class": "tdbold"}})

    class Meta:
        model = Battery
        sequence = ('pic', 'name', 'price_rub', 'price', 'ru_stock',
                    's_config', 'capacity', 'discharge', 'amps',
                    'weight', 'cap_to_weight', 'cap_to_price', '...')
        exclude = ('id', 'created', 'modified', 'link')
