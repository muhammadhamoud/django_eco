
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit-profile'),
    
    path('register/', views.register_view, name='register'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout'),
    path('reset-password/', views.reset_password_with_email, name='reset-password'),
    path('password-reset-check/<str:uidb64>/<str:token>/', views.password_token_check, name='password-reset-check'),
    path('set-new-password/<str:uidb64>/<str:token>/', views.set_new_password, name='set-new-password'),
    # path('users/', views.user_list_view, name='user-list'),
    # Add more URL patterns as needed
]

