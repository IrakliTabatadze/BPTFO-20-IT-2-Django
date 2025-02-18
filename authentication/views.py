from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')

        else:
            return render(request, 'registration/registration.html', {'form': form})
    else:
        form = RegistrationForm()

        return render(request, 'registration/registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect('event_list')
            else:
                return redirect('login')

    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)

    return redirect('login')