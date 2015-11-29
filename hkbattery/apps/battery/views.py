from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views import generic
from django_tables2 import RequestConfig
from .models import Battery
from .filters import BatteryFilter
from .tables import BatteryTable


class TableTemplateView(generic.TemplateView):
    template_name = 'battery/index.html'

    def get_queryset(self, **kwargs):
        return Battery.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TableTemplateView, self).get_context_data(**kwargs)
        filter = BatteryFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = BatteryFilter().helper
        table = BatteryTable(filter.qs)
        RequestConfig(self.request, paginate={'per_page': 25}).configure(table)
        context['filter'] = filter
        context['table'] = table
        context['filter_vals'] = Battery.min_max.values()
        return context


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


class CompareView(generic.View):

    def get(self, request):
        template_name = 'battery/compare.html'
        if request.GET.get('compare'):
            item_pks = request.GET.getlist('compare')
            table = BatteryTable(Battery.objects.filter(pk__in=item_pks))
            RequestConfig(request).configure(table)
            return render(request, template_name, {'table': table})
        else:
            return redirect(reverse('battery:index'))
