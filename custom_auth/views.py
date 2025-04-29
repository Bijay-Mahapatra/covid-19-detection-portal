from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({
                'success': True,
                'username': user.username,
                'first_name': user.first_name,
                'profile_image': user.profile_image.url if user.profile_image else None
            })
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        })
    return JsonResponse({'success': False})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({
                'success': True,
                'username': user.username,
                'first_name': user.first_name,
                'profile_image': user.profile_image.url if user.profile_image else None
            })
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        })
    return JsonResponse({'success': False})

@login_required
@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})

@csrf_exempt
def check_auth(request):
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'first_name': request.user.first_name if request.user.is_authenticated else None,
        'profile_image': request.user.profile_image.url if request.user.is_authenticated and request.user.profile_image else None
    })

class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot_password.html'
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'  # Reference HTML template
    subject_template_name = 'registration/password_reset_subject.txt'

    def form_valid(self, form):
        try:
            super().form_valid(form)
            logger.info(f"Password reset email sent for {form.cleaned_data['email']}")
            return JsonResponse({
                'success': True,
                'message': 'If an account exists with this email, a reset link has been sent.'
            })
        except Exception as e:
            logger.error(f"Error sending reset email to {form.cleaned_data['email']}: {str(e)}")
            return JsonResponse({
                'success': True,  # Maintain security by not revealing email existence
                'message': 'If an account exists with this email, a reset link has been sent.'
            })

    def form_invalid(self, form):
        logger.warning(f"Invalid password reset form: {form.errors}")
        return JsonResponse({
            'success': False,
            'errors': {'email': [{'message': form.errors.get('email', ['Invalid email'])[0]}]}
        }, status=400)
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = ResetPasswordForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            user = self.user
            user.set_password(form.cleaned_data['new_password1'])
            user.clear_reset_token()
            user.save()
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            })
        return super().form_invalid(form)