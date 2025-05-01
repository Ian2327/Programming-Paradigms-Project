from django.contrib import admin
from .models import User, Listing, Image, Message
from .forms import LoginForm, CreateUserForm

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Image)
admin.site.register(Message)
