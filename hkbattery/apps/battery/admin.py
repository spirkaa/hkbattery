from django.contrib import admin
from .models import Battery


class BatteryAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ('name',)
    list_display = ('name',
                    'price',
                    'ru_stock',
                    'capacity',
                    's_config',
                    'discharge',
                    'weight',
                    'created',
                    'modified',
                    'id')

    list_filter = ('s_config',
                   'capacity',
                   'discharge',
                   'created',
                   'modified')

    fieldsets = [
        (None,              {'fields': ['link',
                                        'name',
                                        'price',
                                        'ru_stock']}),
        ('Image',           {'fields': ['pic']}),
        ('Battery specs',   {'fields': [('capacity',
                                         's_config',
                                         'discharge',
                                         'charge',)]}),
        ('Calculations',    {'fields': [('amps',
                                         'cap_to_price',
                                         'cap_to_weight')]}),
        ('Dimensions',      {'fields': [('weight',
                                         'length',
                                         'height',
                                         'width')]})
    ]

admin.site.register(Battery, BatteryAdmin)
