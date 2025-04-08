from django.urls import path
from . import views

app_name = 'campusmart'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout')
]