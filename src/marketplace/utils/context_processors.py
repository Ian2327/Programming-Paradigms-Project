from campusmart.models import Listing, User
from django.utils import timezone
from django.shortcuts import redirect
def get_listings(request):
    if 'user' not in request.session: #redirect to login if not logged in
        return {'listing_remaining':0}

    username = request.session['user']
    user = User.objects.get(username=username)
    today = timezone.now()

    listings_today = Listing.objects.filter(seller=user, date=today)
    listings_remaining = 3 - listings_today.count() + user.extra_listings_remaining
    return {'listings_remaining':listings_remaining}