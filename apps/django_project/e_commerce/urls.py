"""e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.products.models import Category, Product, Order, Order_Product, Address
from django.conf.urls.static import static
import settings

class CategoryAdmin(admin.ModelAdmin):
	pass
admin.site.register(Category, CategoryAdmin)
class ProductAdmin(admin.ModelAdmin):
	pass
admin.site.register(Product, ProductAdmin)
class OrderAdmin(admin.ModelAdmin):
	pass
admin.site.register(Order, OrderAdmin)
class Order_ProductAdmin(admin.ModelAdmin):
	pass
admin.site.register(Order_Product, Order_ProductAdmin)
class AddressAdmin(admin.ModelAdmin):
	pass
admin.site.register(Address, AddressAdmin)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)