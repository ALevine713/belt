from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^new_wish$', views.new_wish),
    url(r'^add_wish$', views.add_wish),
    url(r'^include_wish/(?P<wish_id>\d+)$', views.include_wish),
    url(r'^remove_wish/(?P<wish_id>\d+)$', views.remove_wish),
    url(r'^delete/(?P<wish_id>\d+)$', views.delete),
    url(r'^wish/(?P<wish_id>\d+)$', views.include_wish),
    url(r'^wish_info/(?P<wish_id>\d+)$', views.wish_info),
]
