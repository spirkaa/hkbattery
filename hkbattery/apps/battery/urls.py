from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^data.json$', views.JsonView.as_view(), name='data'),
    url(r'^table/$', views.TableView.as_view(), name='table'),
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^filter/$', views.FilterView.as_view(), name='filter'),
    url(r'^update$', views.update, name='update'),
]
