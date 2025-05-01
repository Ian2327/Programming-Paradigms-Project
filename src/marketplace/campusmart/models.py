from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)
    extra_listings_remaining = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Listing(models.Model):
    conditionChoices = [
        ("N", "New"),
        ("L" , "Like New"),
        ("V" , "Very Good"),
        ("G" , "Good"),
        ("A" , "Acceptable"),
        ("F" , "Fair"),
        ("P" , "Poor")
    ]
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    condition = models.CharField(max_length=1, choices=conditionChoices, default="G")
    available_status = models.BooleanField(default=True)
    date = models.DateField(default=timezone.now)
    primary_photo = models.ImageField(upload_to='')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Image(models.Model):
    image = models.ImageField(upload_to='')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=4000)
    time = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    
    def mark_as_read(self):
        self.read = True
        self.save()

    def __str__(self):
        return f"{self.sender.username}: {self.message}"
