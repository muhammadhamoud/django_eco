# views.py
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import jwt
from .models import CustomUser
from authentication.auth_services.utils import EmailTemplates, Util
# from services.customPermission import IsAdminUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EditProfileForm, PasswordResetForm, SetNewPasswordForm

User = get_user_model()

@login_required
def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        context = {'user': user}
        return render(request, 'profile.html', context)
    else:
        return redirect('login')


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successfully saving the form
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save()

            token = jwt.encode({'user_id': user.id}, 'your_secret_key', algorithm='HS256')
            
            abs_url = f'https://{settings.WEBISTE_NAME}/verify-email/?token=' + token

            email_body_html = EmailTemplates.email_verfication_template(user.email, abs_url)

            data = {'to_email': user.email, 'email_body': email_body_html, 'email_subject': 'Verify your email'}
            Util.send_email(data)

            login(request, user)
            return redirect('edit_profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


# def register_view(request):
#     if request.method == 'POST':
#         user_data = request.POST
#         user = CustomUser.objects.create_user(email=user_data['email'], password=user_data['password'])
#         user.save()

#         token = jwt.encode({'user_id': user.id}, 'your_secret_key', algorithm='HS256')
#         abs_url = 'http://example.com/verify-email/?token=' + token

#         email_body_html = EmailTemplates.email_verfication_template(user.email, abs_url)

#         data = {'to_email': user.email, 'email_body': email_body_html, 'email_subject': 'Verify your email'}
#         Util.send_email(data)

#         return HttpResponse('User registered successfully. Please check your email to verify your account.', status=201)


def verify_email(request):
    token = request.GET.get('token')

    try:
        payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        user = CustomUser.objects.get(id=payload['user_id'])
        if not user.is_verified:
            user.is_verified = True
            user.save()
        return render(request, 'verification_success.html')  # Render the success template

    except jwt.exceptions.DecodeError as err:
        return render(request, 'verification_failure.html')  # Render the failure template
    

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Replace 'profile' with the desired profile page URL
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

    # if request.method == 'POST':
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     user = authenticate(request, email=email, password=password)
    #     if user:
    #         login(request, user)
    #         return HttpResponse('Login successful', status=200)
    #     else:
    #         return HttpResponse('Invalid credentials', status=401)


def reset_password_with_email(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(CustomUser, email=email)

            uidb64 = urlsafe_base64_encode(smart_str(user.id).encode('utf-8'))  # Encode as bytes
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request=request).domain

            relative_link = reverse('password-reset-check', kwargs={'uidb64': uidb64, 'token': token})
            abs_url = 'http://' + current_site + relative_link

            email_body = 'Hi,\nUse the link below to reset your password:\n{}'.format(abs_url)
            data = {'to_email': user.email, 'email_body': email_body, 'email_subject': 'Reset your password'}
            Util.send_email(data)

            return render(request, 'password_reset_success.html') 

    else:
        form = PasswordResetForm()

    return render(request, 'reset_password.html', {'form': form})

def password_token_check(request, uidb64, token):
    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=id)

        if not default_token_generator.check_token(user, token):
            return HttpResponse('Token is not valid, please request a new one', status=401)

        # Redirect to the set new password form
        return redirect('set-new-password', uidb64=uidb64, token=token)
    except DjangoUnicodeDecodeError as err:
        return HttpResponse('Token is not valid, please request a new one', status=401)
    

def set_new_password(request, uidb64, token):
    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=id)

        if not default_token_generator.check_token(user, token):
            return HttpResponse('Token is not valid, please request a new one', status=401)

        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                return redirect('login')  # Redirect to login page after successful password reset
        else:
            form = SetNewPasswordForm()

        return render(request, 'set_new_password.html', {'form': form})

    except DjangoUnicodeDecodeError as err:
        return HttpResponse('Token is not valid, please request a new one', status=401)



def logout_view(request):
    logout(request)
    return redirect('login')



# @IsAdminUser
# def user_list_view(request):
#     if request.method == 'GET':
#         users = CustomUser.objects.all()
#         users_data = [{'id': user.id, 'email': user.email} for user in users]
#         return JsonResponse(users_data, safe=False)



# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from django.contrib.auth.decorators import login_required

# from ..users.forms import CustomUserCreationForm, CustomAuthenticationForm

# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('profile')  # Replace 'profile' with the desired profile page URL
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('profile')  # Replace 'profile' with the desired profile page URL
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'login.html', {'form': form})


# # Add views for email verification, refresh token, and password reset as needed


# @login_required
# def profile_view(request):
#     user = request.user
#     # Customize this part to fetch additional user profile data if needed
#     context = {'user': user}
#     return render(request, 'profile.html', context)