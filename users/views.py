from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from .forms import UserRegisterForm
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for "{username}"')
            return redirect('login')

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('homepage'))

        else:
            form = UserRegisterForm()
            return render(request, "users/register.html", {'form': form})


class LoginFormView(SuccessMessageMixin, auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"
    success_url = '/'
    success_message = "Successfully Logged in"


def logout_view(request):
    logout(request)
    return redirect('homepage')


class CustomPasswordResetView(PasswordResetView):
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