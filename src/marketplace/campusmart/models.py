from django.db import models
from django import forms

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)
    is_authenticated = False

    def __str__(self):
        return self.name

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

class CreateUserForm(forms.Form):
    name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
    password_auth = forms.CharField(widget=forms.PasswordInput)
