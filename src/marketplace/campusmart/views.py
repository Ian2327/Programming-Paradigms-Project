from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from .models import User


# Create your views here.
from .models import LoginForm

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('campusmart:home')
            else:
                error_message = "The username/password combination does not match our records."

    return render(request, 'campusmart/login.html', {'form': form, 'error_message': error_message})


def home(request):
    return render(request, 'campusmart/home.html')

def logout(request):
    # remove the logged-in user information
    auth_logout(request)
    return redirect('campusmart:home') 