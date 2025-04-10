from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import User


# Create your views here.
from .models import LoginForm, CreateUserForm

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username)

            if len(user) > 0 and check_password(password, user[0].password):
                # create a new session
                request.session["user"] = username
                return HttpResponseRedirect(reverse('campusmart:home'))
            else:
                error_message = "The username/password combination does not match our records."

    return render(request, 'campusmart/login.html', {'form': form, 'error_message': error_message})

def create_user_view(request):
    form = CreateUserForm(request.POST or None)
    error_messages = []

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_auth = form.cleaned_data['password_auth']
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                error_messages.append("Username already in use.")
                
            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                error_messages.append("Email already in use.")
                
            # Check if the passwords match
            if password != password_auth:
                error_messages.append("Passwords do not match.")
                
            if not error_messages:
                # Create the user and save it to the database
                user = User(
                    name=name,
                    username=username,
                    email=email,
                    password=make_password(password),  # Hash the password before saving
                )
                user.save()
                messages.success(request, "User created successfully!")
                return redirect('campusmart:login')

    return render(request, 'campusmart/create_user.html', {'form': form, 'error_messages': error_messages})


def home(request):
    return render(request, 'campusmart/home.html')

def logout(request):
    # remove the logged-in user information
    auth_logout(request)
    return redirect('campusmart:home') 
