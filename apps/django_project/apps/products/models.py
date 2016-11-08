from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

SIZE_CHOICES = (
	('xs', 'xs'),
	('small', 'small'),
	('med', 'med'),
	('large', 'large'),
	('xl', 'xl'),
) 

STATUS_CHOICES = (
	('Received', 'Received'),
	('Processed', 'Processed'),
	('Shipped', 'Shipped'),
	)
class Category(models.Model):
	name = models.CharField(max_length=22)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
	name = models.CharField(max_length=22)
	description = models.TextField()
	category = models.ForeignKey(Category)
	inventory = models.IntegerField()
	sold = models.IntegerField()
	price = models.DecimalField(max_digits=7, decimal_places=2)
	size = models.CharField(max_length=10, choices=SIZE_CHOICES)
	image = models.ImageField(upload_to='pics/', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
	user = models.ForeignKey(User)
	total = models.DecimalField(max_digits=6, decimal_places=2)
	status = models.CharField(max_length=255, choices=STATUS_CHOICES)
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

