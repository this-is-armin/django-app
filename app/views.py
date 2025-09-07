from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.views import View

from .forms import UserSignUpForm, UserSignInForm, UserUpdateForm, UserDeleteForm
from .mixins import AnonymousRequiredMixin, OwnerRequiredMixin


User = get_user_model()


# ---------------------------------------------------------------
# section: <BASE>
# ---------------------------------------------------------------

class HomeView(View):
	template_name = 'base/index.html'

	def get(self, request):
		return render(request, self.template_name)

# ---------------------------------------------------------------
# section: </BASE>
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# section: <ACCOUNT>
# ---------------------------------------------------------------

class UserSignUpView(AnonymousRequiredMixin, View):
	template_name = 'account/sign-up.html'
	form_class = UserSignUpForm

	def get(self, request):
		return render(request, self.template_name, {
			'form' : self.form_class(),
		})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
			messages.success(request, 'Successfully signed up', 'info')
			return redirect('app:user_sign_in')
		return render(request, self.template_name, {
			'form' : form,
		})


class UserSignInView(AnonymousRequiredMixin, View):
	template_name = 'account/sign-in.html'
	form_class = UserSignInForm

	def get(self, request):
		return render(request, self.template_name, {
			'form' : self.form_class(),
		})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])

			if user is not None:
				login(request, user)
				messages.success(request, 'Successfully signed in', 'info')
				return redirect('app:home')
			messages.error(request, 'Incorrect Username or Password', 'danger')
			return redirect('app:user_sign_in')
		return render(request, self.template_name, {
			'form' : form,
		})


class UserSignOutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'Successfully signed out', 'info')
		return redirect('app:home')


class UserDeleteView(LoginRequiredMixin, OwnerRequiredMixin, View):
	template_name = 'account/user-delete.html'
	form_class = UserDeleteForm
	
	def get(self, request, **kwargs):
		return render(request, self.template_name, {
			'form': self.form_class(),
		})
	
	def post(self, request, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			user = get_object_or_404(User, username=kwargs['username'])

			if user.username == cd['username']:
				user.delete()
				messages.success(request, 'Successfully deleted account', 'info')
				return redirect('app:home')
			messages.error(request, 'Incorrect Username', 'danger')
			return redirect('app:user_delete', request.user.username)
		return render(request, self.template_name, {
			'form': form,
		})


class UserPageView(LoginRequiredMixin, View):
	template_name = 'account/user-page.html'

	def get(self, request, **kwargs):
		user = get_object_or_404(User, username=kwargs['username'])
		return render(request, self.template_name, {
			'user' : user,
		})


class UserUpdateView(LoginRequiredMixin, OwnerRequiredMixin, View):
	template_name = 'account/user-update.html'
	form_class = UserUpdateForm

	def setup(self, request, *args, **kwargs):
		self.user_instance = get_object_or_404(User, username=kwargs['username'])
		return super().setup(request, *args, **kwargs)

	def get(self, request, **kwargs):
		user = self.user_instance
		return render(request, self.template_name, {
			'form': self.form_class(initial={
				'username' : user.username,
				'email' : user.email,
			}),
		})

	def post(self, request, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = self.user_instance
			cd = form.cleaned_data

			if User.objects.filter(username=cd['username']).exclude(username=cd['username']).exists():
				form.add_error('This username already exists')
			else:
				user.username = cd['username']
				user.email = cd['email']
				user.save()
				messages.success(request, 'Successfully updated account', 'info')
				return redirect('app:user_page', user.username)
		return render(request, self.template_name, {
			'form' : form,
		})

# ---------------------------------------------------------------
# section: </ACCOUNT>
# ---------------------------------------------------------------