import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div
from crispy_forms.bootstrap import InlineField
from .models import Battery


class BatteryFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_type='icontains')
    price = django_filters.RangeFilter()
    ru_stock = django_filters.RangeFilter(label='RU stock')
    s_config = django_filters.RangeFilter(label='S config')
    capacity = django_filters.RangeFilter(label='Capacity (mAh)')
    weight = django_filters.RangeFilter(label='Weight (g)')
    discharge = django_filters.RangeFilter(label='Discharge (C)')
    charge = django_filters.RangeFilter(label='Charge (C)')

    class Meta:
        model = Battery
        # fields = ['name', 'price', 's_config', 'capacity', 'weight', 'amps']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'get'
        helper.help_text_inline = True
        helper.form_class = 'form-inline'
        helper.field_template = 'bootstrap3/layout/inline_field.html'
        helper.layout = Layout(
                            'name',
                            'price',
                            'ru_stock',
                            's_config',
                            'capacity',
                            'weight',
                            'discharge',
                            'charge',
                        Submit('filter', 'Filter'))

        return helper
