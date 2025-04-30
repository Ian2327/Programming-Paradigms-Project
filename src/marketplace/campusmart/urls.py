from django.urls import path
from . import views

app_name = 'campusmart'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('paywall/', views.paywall, name='paywall'),
    path('buy_coin/', views.buy_coin_view, name='buy_coins'),
    path('view-listings/', views.listings, name='listings'),
    path('search-results/', views.search_results, name='search_results'),
    path('checkout/', views.user_pay, name='checkout')
]
