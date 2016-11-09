from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product

# Create your views here.

def listing(request):
    product_list = Product.objects.all()
    categories = Category.objects.all()

    paginator = Paginator(product_list, 6) # Show 6 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {'products': products, 'categories': categories}

    return render(request, 'pagination_app/index.html', context)

def index(request):
	cats = Category.objects.all()
	prods = Product.objects.all()

	context = {'cats': cats,
	'prods': prods}
	return render(request, 'pagination_app/index.html', context)

def category(request):
	cat_name = request.POST['name']
	Category.objects.addcategory(cat_name)
	
	return redirect('/')

def product(request):
	prod_name = request.POST['name']
	prod_desc = request.POST['description']
	prod_cat = Category.objects.get(id=request.POST['category'])

	Product.objects.addproduct(prod_name, prod_desc, prod_cat)
	
	return redirect('/')
