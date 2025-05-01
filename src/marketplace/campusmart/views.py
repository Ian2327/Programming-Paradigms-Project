from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Listing, Message
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import BuyListingForm
import requests
from django.views.generic import DetailView


# Create your views here.
from .forms import LoginForm, CreateUserForm, CreateListingForm, ListingImageForm, EditListingForm

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
    del request.session['user']
    return redirect('campusmart:home') 

def create_listing(request):
    if 'user' not in request.session: #redirect to login if not logged in
        return redirect('campusmart:login')

    username = request.session['user']
    user = User.objects.get(username=username)
    today = timezone.now()

    listings_today = Listing.objects.filter(seller=user, date=today)
    listings_remaining = 3 - listings_today.count() + user.extra_listings_remaining
    print(listings_remaining)
    


    if request.method == 'POST':    
        parentForm = CreateListingForm(request.POST, request.FILES)
        if len(listings_today) >= 3: # redirect to pay prompt if over the limit
            if user.extra_listings_remaining <= 0:
                print(user.extra_listings_remaining)
                return redirect('campusmart:paywall')
            print(user.extra_listings_remaining)
            user.extra_listings_remaining -= 1
            print(user.extra_listings_remaining)
            user.save()
        factoryForm = ListingImageForm(request.POST, request.FILES)
        if parentForm.is_valid() and factoryForm.is_valid():

            title = parentForm.cleaned_data['title']
            description = parentForm.cleaned_data['description']
            price = parentForm.cleaned_data['price']
            image = parentForm.cleaned_data['image']
            listing = Listing(
                    title=title,
                    description=description,
                    price=price,
                    condition=parentForm.cleaned_data['condition'],
                    seller=user,
                    primary_photo=image
                )
            listing.save()
            factoryForm.instance = listing
            factoryForm.save()
            messages.success(request, "Listing created successfully!")
            return redirect('campusmart:home')
    else:
        parentForm = CreateListingForm()
        factoryForm = ListingImageForm()
    return render(request, 'campusmart/create_listing.html', {'parentForm': parentForm, 'factoryForm' : factoryForm, 'listingsRemain':listings_remaining} )

def paywall(request):
    return render(request, 'campusmart/paywall.html')

def listings(request):
    all_listings = Listing.objects.all().order_by('-date')

    paginator = Paginator(all_listings, 20)
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    context = {'listings':listings,}

    return render(request, 'campusmart/view_listings.html', context)

def search_results(request):
    all_listings = Listing.objects.all().order_by('-date')
    query = request.GET.get('query', '')
    filtered_listings_title = all_listings.filter(title__icontains=query)
    filtered_listings_description = all_listings.filter(description__icontains=query)
    filtered_listings = filtered_listings_title|filtered_listings_description

    paginator = Paginator(filtered_listings, 20)
    page = request.GET.get('page')
    try:
        filtered_listings = paginator.page(page)
    except PageNotAnInteger:
        filtered_listings = paginator.page(1)
    except EmptyPage:
        filtered_listings = paginator.page(paginator.num_pages)

    context = {'filtered_listings':filtered_listings,}

    return render(request, 'campusmart/search_results.html', context)

def my_listings(request):
    if 'user' not in request.session: #redirect to login if not logged in
        return redirect('campusmart:login')
    
    username = request.session['user']
    user = User.objects.get(username=username)
    
    my_listings = Listing.objects.all().filter(seller=user).order_by('-date')

    paginator = Paginator(my_listings, 20)
    page = request.GET.get('page')
    try:
        filtered_listings = paginator.page(page)
    except PageNotAnInteger:
        filtered_listings = paginator.page(1)
    except EmptyPage:
        filtered_listings = paginator.page(paginator.num_pages)

    context = {'filtered_listings':filtered_listings,}

    return render(request, 'campusmart/my_listings.html', context)

def edit_listing(request, pk):
    if 'user' not in request.session: #redirect to login if not logged in
        return redirect('campusmart:login')

    username = request.session['user']
    user = User.objects.get(username=username)
    listing = get_object_or_404(Listing, id=pk)
    if listing.seller != user:
        messages.error(request, 'You do not own this item')
        return redirect('campusmart:home')

    if request.method == 'POST':
        parentForm = EditListingForm(request.POST, request.FILES, instance=listing)
        factoryForm = ListingImageForm(request.POST, request.FILES, instance=listing)

        if parentForm.is_valid() and factoryForm.is_valid():

                listing.save()
                factoryForm.save()
                messages.success(request, "Listing edited successfully!")
                return redirect('campusmart:home')
    
    else:
        parentForm = EditListingForm(instance=listing)
        factoryForm = ListingImageForm(instance=listing)

    return render(request, 'campusmart/edit_listing.html', {'parentForm': parentForm, 'factoryForm' : factoryForm} )


def delete_listing(request, pk):

    if 'user' not in request.session: #redirect to login if not logged in
        return redirect('campusmart:login')

    username = request.session['user']
    user = User.objects.get(username=username)
    listing = get_object_or_404(Listing, id=pk)
    if listing.seller != user:
        messages.error(request, 'You do not own this item')
        return redirect('campusmart:home')

    listing.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('campusmart:home')

def user_listings(request):
    user = User.objects.get(username=request.session['user'])
    all_listings = Listing.objects.all().filter(seller=user).order_by('-date')

    paginator = Paginator(all_listings, 20)
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    context = {'listings':listings,'can_delete':True}

    return render(request, 'campusmart/view_listings.html', context)

def buy_coin_view(request):
    if 'user' not in request.session: #redirect to login if not logged in
        return redirect('campusmart:login')
    username = request.session['user']
    error_message = None
    user = User.objects.get(username=username)
    currUser = ""
    print(user)
    today = timezone.now()
    currAmount = view_balance_for_user("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0NTA1NTg0LCJpYXQiOjE3NDU4NjU1ODQsImp0aSI6IjA5MmZhZDQ5ZGZhOTQyZTg5YTU4YjZhMzBlOWRmNjM5IiwidXNlcl9pZCI6Njh9.r9stWOk9hhqYJCDgn2QRddonoxhyZrKtdGxOJZ9vIJI", user.email)
    if currAmount == None:
        amt = 0;
    else:
        amt = currAmount["amount"]

    
    
    if request.method == "POST":
        form = BuyListingForm(request.POST)
        if form.is_valid():
            if type(user_pay("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0NTA1NTg0LCJpYXQiOjE3NDU4NjU1ODQsImp0aSI6IjA5MmZhZDQ5ZGZhOTQyZTg5YTU4YjZhMzBlOWRmNjM5IiwidXNlcl9pZCI6Njh9.r9stWOk9hhqYJCDgn2QRddonoxhyZrKtdGxOJZ9vIJI", user.email, form.cleaned_data['amount'])) != dict:
                error_message="Insufficent Funds"
            else:
                user.extra_listings_remaining+=form.cleaned_data['amount']
                user.save()
                return HttpResponseRedirect("/buy_coin" )
    else:
        form = BuyListingForm()
    context = {
        'amt':amt,
        'email':user.email,
        'form':form,
        'error_message':error_message
        
    }
    
    return render(request, "campusmart/buy_coins.html",context=context)

def view_balance_for_user(access_token, email):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }


   # Make a GET request with the authorization header
   api_response = requests.get(f"https://jcssantos.pythonanywhere.com/api/group10/group10/player/{email}/", headers=headers)


   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to view balance for user:", api_response.status_code)
def user_pay(access_token, email, amount):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }
   data = {"amount": amount} # non-negative integer value to be decreased
   # Make a POST request with the authorization header and data payload
   api_response = requests.post(f"https://jcssantos.pythonanywhere.com/api/group10/group10/player/{email}/pay", headers=headers, data=data)


   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to pay:", api_response.status_code)

class listing_detail(DetailView):
    model = Listing
    template_name = 'listing_detail.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.request.session['user'])

        context = super().get_context_data(**kwargs)
        if 'user' in self.request.session:
            user = User.objects.get(username=self.request.session['user'])
            if user == self.object.seller:
                context['can_delete'] = True
        return context

def messages_view(request):
    if 'user' not in request.session: #redirect to login if not logged in
        return redirect('campusmart:login')
    username = request.session['user']
    user = User.objects.get(username=username)
    messages = user.receiver.all() | user.sender.all()
    messages = messages.order_by('time')
    recent_messages = {}
    for message in messages:
        other_user = message.sender if message.sender != user else message.receiver
        if other_user not in recent_messages or message.time > recent_messages[other_user].time:
            recent_messages[other_user] = message
    context = {'recent_messages': sorted(recent_messages.items(), key=lambda x: x[1].time, reverse=True), 'current_user': user}
    return render(request, 'campusmart/messages.html', context)

def chat_view(request, other_user):
    if 'user' not in request.session: #redirect to login if not logged in
        return redirect('campusmart:login')
    username = request.session['user']
    user = User.objects.get(username=username)
    other_user = User.objects.get(username=other_user)
    messages = user.receiver.filter(sender=other_user) | user.sender.filter(receiver=other_user)
    messages = messages.order_by('time')
    item = request.GET.get('item')
    
    for message in messages:
        if message.receiver == user and not message.read:
            message.mark_as_read()
            
    if request.method == 'POST':
        message = request.POST.get('message')
        new_message = Message(
            sender=user,
            receiver=other_user,
            message=message
        )
        new_message.save()
        return redirect('campusmart:chat', other_user=other_user.username)
    else:
        return render(request, 'campusmart/chat.html', {'chat': messages, 'other_user': other_user, 'user': user, 'item': item})
