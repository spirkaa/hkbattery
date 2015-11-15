from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TableTemplateView.as_view(), name='index'),
    url(r'^table/$', views.BootstrapTableView.as_view(), name='table'),
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^update$', views.update, name='update'),
]
