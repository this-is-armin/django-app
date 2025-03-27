from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View

from .forms import UserSignUpForm, UserSignInForm, UserUpdateForm


def home(request):
	return render(request, 'base/index.html')


######################################################
# Account(Users) section:

class UserSignUpView(View):
	template_name = 'account/sign-up.html'
	form_class = UserSignUpForm

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated: return redirect('app:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
			messages.success(request, 'Sign-Up was successful', 'info')
			return redirect('app:user_sign_in')
		return render(request, self.template_name, {'form':form})


class UserSignInView(View):
	template_name = 'account/sign-in.html'
	form_class = UserSignInForm

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated: return redirect('app:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])

			if user is not None:
				login(request, user)
				messages.success(request, 'Sign-In was successful', 'info')
				return redirect('app:home')
			messages.error(request, 'Username or Password incorrect', 'danger')
			return redirect('app:user_sign_in')
		return render(request, self.template_name, {'form':form})


def user_signout_view(request):
	if not request.user.is_authenticated: return redirect('app:home')
	logout(request)
	messages.success(request, 'Sign-Out was successful', 'info')
	return redirect('app:home')


def user_delete_view(request, username):
	user = get_object_or_404(User, username=username)
	if not request.user.is_authenticated: return redirect('app:home')
	if request.user != user: return redirect('app:user_page', user.username)
	user.delete()
	messages.success(request, 'Account was deleted successful', 'info')
	return redirect('app:home')


class UserPageView(View):
	template_name = 'account/user-page.html'

	def setup(self, request, *args, **kwargs):
		self.user_instance = get_object_or_404(User, username=kwargs['username'])
		return super().setup(request, *args, **kwargs)

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated: return redirect('app:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request, **kwargs):
		user = self.user_instance
		return render(request, self.template_name, {'user':user})


class UserUpdateView(View):
	template_name = 'account/user-update.html'
	form_class = UserUpdateForm

	def setup(self, request, *args, **kwargs):
		self.user_instance = get_object_or_404(User, username=kwargs['username'])
		return super().setup(request, *args, **kwargs)

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated: return redirect('app:home')
		if request.user != self.user_instance: return redirect('app:user_page', self.user_instance.username)
		return super().dispatch(request, *args, **kwargs)

	def get(self, request, **kwargs):
		user = self.user_instance
		INITIAL = {'email':user.email}
		form = self.form_class(initial=INITIAL)
		return render(request, self.template_name, {'form':form, 'user':user})

	def post(self, request, **kwargs):
		user = self.user_instance
		form = self.form_class(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			user.email = cd['email']
			user.save()
			messages.success(request, 'Account was updated successful', 'info')
			return redirect('app:user_page', user.username)
		return render(request, self.template_name, {'form':form, 'user':user})

#######################################################
