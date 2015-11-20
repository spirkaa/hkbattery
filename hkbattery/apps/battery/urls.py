from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TableTemplateView.as_view(), name='index'),
    url(r'^compare/$', views.CompareView.as_view(), name='compare'),
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^update$', views.update, name='update'),
]
