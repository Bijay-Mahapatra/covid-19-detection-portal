from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
import re

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': _('Enter a valid email address (e.g., user@example.com)')}
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    profile_image = forms.ImageField(required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("Password must contain at least 8 characters, including 1 uppercase letter and 1 number.")
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_image')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email is already registered."))
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least 1 uppercase letter."))
        if not re.search(r'[0-9]', password):
            raise ValidationError(_("Password must contain at least 1 number."))
        return password

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))

class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        error_messages={'invalid': _('Enter a valid email address')}
    )

class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("Password must contain at least 8 characters, including 1 uppercase letter and 1 number.")
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least 1 uppercase letter."))
        if not re.search(r'[0-9]', password):
            raise ValidationError(_("Password must contain at least 1 number."))
        return password