from django.urls import path
from .views import (
    register_view, 
    login_view, 
    logout_view, 
    check_auth,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('check-auth/', check_auth, name='check_auth'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]