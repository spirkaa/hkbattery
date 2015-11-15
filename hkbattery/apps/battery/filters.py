import django_filters
from .models import Battery


class BatteryFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_type='icontains')
    price = django_filters.RangeFilter()
    ru_stock = django_filters.RangeFilter(label='RU stock')
    s_config = django_filters.RangeFilter(label='S config')
    capacity = django_filters.RangeFilter(label='Capacity (mAh)')
    discharge = django_filters.RangeFilter(label='Discharge (C)')
    weight = django_filters.RangeFilter(label='Weight (g)')

    class Meta:
        model = Battery
