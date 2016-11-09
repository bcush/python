from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.


# class CategoryManager(models.Manager):
# 	def addcategory(self, name):
# 		Category.objects.create(name=name)


class Category(models.Model):
	name = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# objects = CategoryManager()


# class ProductManager(models.Manager):
# 	def addproduct(self, name, description, category):
# 		Product.objects.create(name=name, description=description, category=category)


class Product(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	category = models.ForeignKey(Category)
	inventory = models.IntegerField()
	sold = models.IntegerField()
	price = models.DecimalField(max_digits=7, decimal_places=2)
	size = models.CharField(max_length=2)
	image = models.CharField(max_length=254)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# objects = ProductManager()


class Order(models.Model):
	user = models.ForeignKey(User)
	total = models.DecimalField(max_digits=6, decimal_places=2)
	status = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Order_Product(models.Model):
	product_id = models.ForeignKey(Product)
	order_id = models.ForeignKey(Order)
	quantity = models.IntegerField()
	
class Address(models.Model):
	user = models.ForeignKey(User)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=2)
	zip = models.CharField(max_length=15)
	reated_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

