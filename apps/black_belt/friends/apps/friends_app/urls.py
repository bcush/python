from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^friends$', views.friends),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'^remove_friend/(?P<id>\d+)$', views.remove_friend),
    url(r'^user/(?P<id>\d+)$', views.user),
    # url(r'^admin/', admin.site.urls),
]
