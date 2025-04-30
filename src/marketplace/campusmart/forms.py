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
    conditionChoices = [
        ("N", "New"),
        ("L" , "Like New"),
        ("V" , "Very Good"),
        ("G" , "Good"),
        ("A" , "Acceptable"),
        ("F" , "Fair"),
        ("P" , "Poor")
    ]
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=4000, widget=forms.Textarea(attrs={'class':'form-control'}))
    price = forms.DecimalField(decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class':'form-control'}))
    condition = forms.ChoiceField(choices=conditionChoices, widget=forms.Select(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))

ListingImageForm = forms.inlineformset_factory(
    parent_model=Listing,
    model=Image,
    fields=('photo',),
    extra=1,
    can_delete=True
)
class BuyListingForm(forms.Form):
    amount = forms.IntegerField()