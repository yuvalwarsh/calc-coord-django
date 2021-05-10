from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from .forms import UserRegisterForm, CleanedEmailPasswordResetForm
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('homepage')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)

        return valid


class LoginFormView(SuccessMessageMixin, auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"
    success_url = '/'
    success_message = "Successfully Logged in"


def logout_view(request):
    logout(request)
    return redirect('homepage')


class CustomPasswordResetView(PasswordResetView):
    form_class = CleanedEmailPasswordResetForm
    template_name = 'users/password_reset.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(*args, **kwargs)
