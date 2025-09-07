from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


User = get_user_model()


class AnonymousRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'Access Denied', 'danger')
            return redirect('app:home')
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        if request.user != user:
            messages.error(request, 'Access Denied', 'danger')
            return redirect('app:home')
        return super().dispatch(request, *args, **kwargs)


# class OwnerForbiddenMixin:
#     def dispatch(self, request, *args, **kwargs):
#         user = get_object_or_404(User, username=kwargs['username'])
#         if request.user == user:
#             messages.error(request, 'Access Denied', 'danger')
#             return redirect('app:home')
#         return super().dispatch(request, *args, **kwargs)