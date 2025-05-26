from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
	path('', views.home_view, name='home'),

	path('account/sign-up/', views.UserSignUpView.as_view(), name='user_sign_up'),
	path('account/sign-in/', views.UserSignInView.as_view(), name='user_sign_in'),
	path('account/sign-out/', views.user_signout_view, name='user_sign_out'),
	path('account/<username>/', views.UserPageView.as_view(), name='user_page'),
	path('account/<username>/delete/', views.user_delete_view, name='user_delete'),
	path('account/<username>/update/', views.UserUpdateView.as_view(), name='user_update')
]
