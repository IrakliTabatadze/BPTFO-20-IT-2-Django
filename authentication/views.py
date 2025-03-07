from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import CreateView
from django.urls import reverse_lazy

import logging

logger = logging.getLogger(__name__)

# def register_user(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#
#             return redirect('login')
#
#         else:
#             return render(request, 'registration/registration.html', {'form': form})
#     else:
#         form = RegistrationForm()
#
#         return render(request, 'registration/registration.html', {'form': form})


class UserRegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('authentication:login')


# def login_user(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#
#                 return redirect('event_list')
#             else:
#                 return redirect('login')
#         else:
#             # logger.error('Login failed: Wrong username or password.')
#             logger.warning('Login failed: Wrong username or password.')
#             return redirect('login')
#
#     else:
#         form = AuthenticationForm()
#         return render(request, 'registration/login.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('core:event_list')



# def logout_user(request):
#     logout(request)
#
#     return redirect('login')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('authentication:login')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()

            update_session_auth_hash(request, request.user)

            return redirect('event_list')

    else:
        form = PasswordChangeForm(user=request.user)

        return render(request, 'registration/change_password.html', {'form': form})

def reset_password_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            form.save(
                request=request,
                use_https=False,
                email_template_name='registration/reset_password_email.html',
            )

            return HttpResponse('Reset Email Sent Successfully Please Check Your Email To Finish The Process')
    else:
        form = PasswordResetForm()

        return render(request, 'registration/reset_password_request.html', {'form': form})


def reset_password_confirm(request, uidb64, token):
    try:
        id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=id)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()

            else:
                form = SetPasswordForm(user=user)
        else:
            return HttpResponse('Invalid Token')

    except (User.DoesNotExist, ValueError):
        return HttpResponse('Invalid Credentials')

    return render(request, 'registration/reset_password_confirm.html', {'form': form})