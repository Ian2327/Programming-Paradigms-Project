from django import forms
from .models import Listing, Image

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

class CreateUserForm(forms.Form):
    name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
    password_auth = forms.CharField(widget=forms.PasswordInput)

class CreateListingForm(forms.Form):
    conditionChoices = {
        "N" : "New",
        "L" : "Like New",
        "V" : "Very Good",
        "G" : "Good",
        "A" : "Acceptable",
        "F" : "Fair",
        "P" : "Poor"
    }
    title = forms.CharField(max_length=200)
    description = forms.TextInput()
    price = forms.DecimalField(decimal_places=2)
    condition = forms.ChoiceField(choices=conditionChoices)

ListingImageForm = forms.inlineformset_factory(
    parent_model=Listing,
    model=Image,
    fields=('photo',),
    extra=1,
    can_delete=True
)
