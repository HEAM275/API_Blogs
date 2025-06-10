from django.urls import path
from apps.authentication.views import (
    LoginView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    RegisterView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(),
         name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
