from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse 
from django.views.generic.edit import UpdateView
from .forms import RegistrationForm, LoginForm, ProductForm
from .models import Product, Order, Order_Product, Address, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django-cart
from cart.cart import Cart
from .models import Product

# Create your views here.

class HomeView(TemplateView):
	def get(self, request):
		categories = Category.objects.all()
		context = { 'categories': categories }
		return render(request, 'products/bradley/index.html', context)

class RegistrationView(TemplateView):
	def get(self, request):
		form = RegistrationForm()
		context={
			'register':form,
		}
		return render(request, 'products/register.html', context)
	def post(self, request, *args, **kwargs):
		if len(request.POST['first_name']) < 3:
			messages.warning(request, 'First Name must at least 3 characters')
			return redirect('/')
		else:
			first_name = request.POST['first_name']
		if len(request.POST['last_name']) < 3:
			messages.warning(request, 'Last Name must at least 3 characters')
			return redirect(reverse_lazy('home'))
		else:
			last_name = request.POST['last_name']
		if len(request.POST['username']) < 3:
			messages.warning(request, 'Username must at least 3 characters')
			return redirect(reverse_lazy('home'))
		else:
			username = request.POST['username']
		if len(request.POST['password']) < 8:
			messages.warning(request, 'Password must be at least 8 characters long')
			return redirect(reverse_lazy('home'))
		elif request.POST['password'] != request.POST['password_conf']:
			messages.warning(request, 'Passwords do not match!')
			return redirect(reverse_lazy('home'))
		else:
			password = request.POST['password']
		email = request.POST['email']		
		User.objects.create_user(first_name=first_name, last_name=last_name, email=email,password=password,username=username)
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		login(request, user)
		return redirect(reverse_lazy('home'))

class LoginView(TemplateView):
	def get(self, request):
		form = LoginForm()
		context={
			'form': form,
		}
		return render(request, 'products/login.html', context)
	def post(self,request):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			return redirect(reverse_lazy('home'))

def logoutUser(request):
	logout(request)
	return redirect(reverse_lazy('home'))

class AdminView(TemplateView):
	def get(self, request):
		login_form = LoginForm()
		context={
			'form':login_form,
		}
		return render(request, 'products/admin.html', context)
	def post(self,request):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			return redirect(reverse_lazy('my_admin/orders/id'))
		else:
			return redirect(reverse_lazy('my_admin'))

class AdminOrderView(TemplateView):
	def get(self, request, status):
		if status == 'Received':
			orders = Order.objects.filter(status='Received')
		elif status == 'Processed':
			orders = Order.objects.filter(status='Processed')
		elif status == 'Shipped':
			orders = Order.objects.filter(status='Shipped')
		else:
			orders = Order.objects.all()
		address = Address.objects.all()
		context={
			'orders':orders, 
			'address':address,
		}
		return render(request, 'products/admin_orders.html', context)

def order_update(request, id, status):
	update = Order.objects.get(id=id)
	update.status = status
	update.save()
	return redirect('/my_admin/orders/all')


def products(request):
	prod_list = Product.objects.all()
	categories = Category.objects.all()
	paginator = Paginator(prod_list, 4) # Show 6 products per page

	page = request.GET.get('page')

	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		products = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		products = paginator.page(paginator.num_pages)

	# products = Product.objects.filter(category__id=cat_id)
	# categories = Category.objects.values('id')
	# products = Product.objects.values('category_id')

	# context = {'products': products, 'prod_cat_ids': prod_cat_ids}
	context = {'products': products, 'categories': categories}
	# print products
	# print categories
	return render(request, 'products/bradley/productpage.html', context)


def product_page(request, cat_id):
	prod_cat_ids = Product.objects.filter(category_id = cat_id)
	categories = Category.objects.all()
	paginator = Paginator(prod_cat_ids, 4) # Show 6 products per page

	page = request.GET.get('page')

	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		products = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		products = paginator.page(paginator.num_pages)

	# products = Product.objects.filter(category__id=cat_id)
	# categories = Category.objects.values('id')
	# products = Product.objects.values('category_id')

	# context = {'products': products, 'prod_cat_ids': prod_cat_ids}
	context = {'products': products, 'categories': categories}
	# print products
	# print categories
	return render(request, 'products/bradley/product_category_page.html', context)

class AdminProductView(TemplateView):
	def get(self, request):
		products = Product.objects.all()
		context={
			'products':products,
		}
		return render(request, 'products/admin_products.html', context)

class AddProductView(TemplateView):
	def get(self,request):
		form = ProductForm(request.POST or None, request.FILES or None)
		category = Category.objects.all()
		context={
			'form':form,
			'category':category,
		}
		return render(request, 'products/add_products.html', context)
	def post(self, request):
		name = request.POST['name']
		description = request.POST['description']
		category = Category.objects.get(name=request.POST['category'])
		inventory = request.POST['inventory']
		sold = request.POST['sold']
		price = request.POST['price']
		size = request.POST['size']
		image = request.FILES['image']
		Product.objects.create(name = name, description = description, category = category, inventory = inventory, sold = sold, price = price, size = size, image = image)
		return redirect(reverse_lazy('my_admin/products'))

class OrderShowView(TemplateView):
	def get(self, request, id):
		order = Order.objects.get(id = id)
		line_items = Order_Product.objects.filter(order_id = id)
		context={
			'order':order,
			'items':line_items,
		}
		return render(request, 'products/order_show.html', context)

class EditProductView(UpdateView):
	model = Product
	fields = '__all__'
	template_name = 'products/update_product.html'
	success_url = '/my_admin/products'

def delete(request, id):
	Product.objects.get(id =id).delete()
	return redirect('/my_admin/products')

def show(request, prod_id):
	categories = Category.objects.all()
	products = Product.objects.get(id=prod_id)
	similars = Product.objects.filter(category=products.category).exclude(id=products.id)
	context = {'products': products, 'categories': categories, 'similars': similars}
	return render(request, 'products/bradley/show.html', context)



def add_to_cart(request):
	id = request.POST['prod_id']
	cart_quant = request.POST['cart_quant']
	print cart_quant
	product = Product.objects.get(id=id)
	cart = Cart(request)
	cart.add(product, product.price, cart_quant)
	return render(request, 'products/bradley/checkout.html', dict(cart=Cart(request)))

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return render(request, 'products/cart.html', dict(cart=Cart(request)))

def get_cart(request):
    return render(request, 'products/cart.html', dict(cart=Cart(request)))

def checkout(request):
    return render(request, 'products/bradley/checkout.html', dict(cart=Cart(request)))

def summary(request):
	return render(request, 'products/bradley/summary.html')

# Larry's Views


# def goBack(request):
# 	return redirect('/')


# def add_to_cart(request, product_id):
# 	product = get_object_or_404(product, pk=product_id)
# 	cart, created = Cart.objects.get_or_create(user=request.user, active=True)
# 	order, created = ProductOrder.objects.get_or_create(product=product, cart=cart)
# 	order.quanity += 1
# 	order.save()
# 	messages.success(request, "Cart has been Updated!")
# 	return redirect('cart')


# def cart(request):
# 	if request.user.is_authenticated():
# 		cart = Cart.objects.filter(user=request.user.id, active = True)
# 		orders = ProductOrder.objects.filter(cart=cart)
# 		total = 0
# 		count = 0
# 		for order in orders:
# 			total =+ order.product.price * order.quanity
# 			count =+ order.quanity

# 		context = {
# 			'cart': orders,
# 			'total': total,
# 			'count': count,
# 		}
# 		return render(request, 'products/cart.html', context)
# 	else:
# 		return redirect('/')
