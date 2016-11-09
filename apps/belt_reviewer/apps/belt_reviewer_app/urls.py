from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.books),
    url(r'^books/(?P<id>\d+)$', views.books_id),
    url(r'^books/add$', views.books_add),
    url(r'^books/addbook$', views.addbook),
    url(r'^addrating$', views.addrating),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)$', views.users_id),
    # url(r'^admin/', admin.site.urls),
]
