from django import forms
from django.db import models
import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from .models import Battery


class RangeWidgetOne(forms.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (forms.HiddenInput(attrs=attrs), forms.TextInput(attrs=attrs))
        super(RangeWidgetOne, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)


class RangeFieldOne(django_filters.fields.RangeField):
    widget = RangeWidgetOne


class RangeFilterOne(django_filters.RangeFilter):
    field_class = RangeFieldOne


class BatteryFilter(django_filters.FilterSet):

    filter_overrides = {
        models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_type': 'icontains'
            }
        },
        models.DecimalField: {
            'filter_class': RangeFilterOne,
            'help_text': 'raz'
        },
        models.SmallIntegerField: {
            'filter_class': RangeFilterOne
        }
    }

    class Meta:
        model = Battery
        # fields = ['name', 'price', 'ru_stock', 's_config',
        # 'capacity', 'weight', 'discharge', 'amps']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'get'
        helper.form_class = 'form-horizontal'
        helper.form_id = 'filter'
        helper.layout = Layout(
            'name',
            'price',
            'ru_stock',
            's_config',
            'capacity',
            'discharge',
            'amps',
            'weight',
            Submit('filter', 'Filter'))

        return helper
