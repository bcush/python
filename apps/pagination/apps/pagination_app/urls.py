from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^listing$', views.listing),
    url(r'^category$', views.category),
    url(r'^product$', views.product),
]
