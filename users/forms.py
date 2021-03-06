from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        # end-case: gmail equals googlemail
        email = self.cleaned_data['email'].lower().replace("googlemail", "gmail")
        users = User.objects.filter(email=email)
        if users:
            raise forms.ValidationError("This email is already signed")
        return email.lower()


class CleanedEmailPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email'].lower().replace("googlemail", "gmail")
        users = User.objects.filter(email=email)
        if not users:
            raise forms.ValidationError("This email is not signed")
        return email.lower()
