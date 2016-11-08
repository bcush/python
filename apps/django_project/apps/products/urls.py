from django.conf.urls import url, include
from .views import  LoginView, RegistrationView, HomeView, AdminView, AdminOrderView, AdminProductView, AddProductView, OrderShowView, EditProductView
from . import views

urlpatterns = [
	url(r'^$', HomeView.as_view(), name='home'),
	url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^register$', RegistrationView.as_view(), name='register'),
	url(r'^logout$', views.logoutUser, name='logout'),
	url(r'^my_admin$', AdminView.as_view(), name='my_admin'),
	url(r'^my_admin/orders/(?P<status>\w+)$', AdminOrderView.as_view(), name='my_admin/orders'),
	url(r'^my_admin/orders/show/(?P<id>\d+)$', OrderShowView.as_view(), name='orders_show'),
	url(r'^my_admin/products$', AdminProductView.as_view(), name='my_admin/products'),
	url(r'^add_products$', AddProductView.as_view(), name='add_product'),
	url(r'^update/(?P<pk>\d+)$', EditProductView.as_view(), name='update'),
	url(r'^order/update/(?P<id>\d+)/(?P<status>\w+)$', views.order_update, name='order_update'),
	url(r'^products$', views.products, name='products'),
	url(r'^products/category/(?P<cat_id>\d+)$', views.product_page, name='product_page'),
	url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),

	url(r'^products/show/(?P<prod_id>\d+)$', views.show, name='show'),

	# url(r'^cart$', views.cart),
	url(r'^add_to_cart$', views.add_to_cart, name='add_to_cart'),
	url(r'^remove_from_cart/(?P<product_id>\d+)$', views.remove_from_cart, name='remove_from_cart'),
	url(r'^get_cart$', views.get_cart, name='get_cart'),
	url(r'^checkout$', views.checkout, name='checkout'),
	url(r'^summary$', views.summary, name='summary'),
	# url(r'^product/(?P<id>\d+)$', views.product),
	# url(r'^goBack$', views.goBack),

]
