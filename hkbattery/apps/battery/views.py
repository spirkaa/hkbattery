from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django_tables2 import RequestConfig
from .models import Battery, run_db_oper, min_max_values
from .filters import BatteryFilter
from .tables import BatteryTable


class FilterView(generic.View):

    def get(self, request):
        return render(request, 'battery/filter.html',
                      {'filter_vals': min_max_values()})


class IndexView(generic.View):

    def get(self, request):
        return render(request, 'battery/index.html',
                      {'batteries': Battery.objects.all()[:50]})


class JsonView(generic.View):

    def get(self, request):
        jsonser = serializers.serialize('json', Battery.objects.all()[:5])
        return JsonResponse(jsonser, safe=False)


class ListView(generic.ListView):

    model = Battery
    template_name = 'battery/list.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        batteries = Battery.objects.all()
        paginator = Paginator(batteries, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            batteries = paginator.page(page)
        except PageNotAnInteger:
            batteries = paginator.page(1)
        except EmptyPage:
            batteries = paginator.page(paginator.num_pages)

        context['batteries'] = batteries
        return context


class TableView(generic.TemplateView):
    template_name = 'battery/table.html'

    def get_queryset(self, **kwargs):
        return Battery.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data(**kwargs)
        filter = BatteryFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = BatteryFilter().helper
        table = BatteryTable(filter.qs)
        RequestConfig(self.request, paginate={'per_page': 25}).configure(table)
        context['filter'] = filter
        context['table'] = table
        context['filter_vals'] = min_max_values()
        # messages.info(self.request, 'test')
        return context


def update(request):
    # run_db_oper('populate')
    return redirect(reverse('battery:index'))
