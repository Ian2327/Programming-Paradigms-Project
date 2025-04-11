from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)
    is_authenticated = False

    def __str__(self):
        return self.name


class Listing(models.Model):

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    condition = models.CharField(max_length=10)
    available_status = models.BooleanField(default=True)
   # seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Image(models.Model):
    photo = models.ImageField(upload_to='')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
