from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Product

class DateInput(forms.DateInput):
	    input_type = 'date'

class TimeInput(forms.DateInput):
	input_type = 'time'

class PasswordInput(forms.PasswordInput):
	input_type = 'password'

class RegistrationForm(ModelForm):
	
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password']
		widgets ={
			'password': PasswordInput()
		}


class LoginForm(ModelForm):

	class Meta:
		model = User
		fields=['username', 'password']
		widgets ={
			'password': PasswordInput()
		} 

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['name', 'description', 'inventory', 'sold', 'price', 'size', 'image']