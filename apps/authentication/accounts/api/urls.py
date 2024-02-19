from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('verify-email', views.VerifyEmail.as_view(), name='verify-email'),
    path('login', views.LoginApiView.as_view(), name='login'),

    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('request-reset-password', views.ResetPasswordWithEmail.as_view(), name='request-reset-password'),
    path('password-reset/<uidb64>/<token>', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('token-validation/', views.TokenValidationView.as_view(), name='token_validation'),

    path('password-reset-complete', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    
    path('get_user/', views.CurrentUsersAPIView.as_view(), name='get_user'),
    path('users', views.UserListAPIView.as_view(), name='all-users'),
    path('<int:id>', views.UserDetailsAPIView.as_view(), name="single-user"),
]


