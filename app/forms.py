from django import forms 
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

import re


User = get_user_model()


def form_field_validator(value, field_name):
	if not value:
		return None
	
	if not re.fullmatch(r'^[a-z0-9_.]+$', value):
		raise ValidationError(f'{field_name} must contain only lowercase letters, numbers, underline and dot.')	
	return value


class UserSignUpForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Username',
	}))
	email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Email Address',
	}))
	password1 = forms.CharField(label='Password', max_length=150, widget=forms.PasswordInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Password',
	}))
	password2 = forms.CharField(label='Confirm Password', max_length=150, widget=forms.PasswordInput(attrs={
		'class':'form-control', 
		'placeholder':'Confirm Password',
	}))

	def clean_username(self):
		username = self.cleaned_data.get('username')
		form_field_validator(username, 'Username')

		if User.objects.filter(username=username).exists():
			raise ValidationError('This username already exists.')
		return username

	def clean(self):
		cd = self.cleaned_data
		p1 = cd.get('password1')
		p2 = cd.get('password2')

		if p1 and p2 and p1 != p2:
			raise ValidationError('Passwords must match.')
		

class UserSignInForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Username',
	}))
	password = forms.CharField(label='Password', max_length=150, widget=forms.PasswordInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Password',
	}))


class UserUpdateForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Username',
	}))
	email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Email Address',
	}))


class UserDeleteForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class':'form-control', 
		'placeholder':'Your Username',
	}))