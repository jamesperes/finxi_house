from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth.models import Permission

import geocoder


class BasicUserMod(AbstractUser):
    """Basic User used base on models users """

    email = models.EmailField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=40, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Seller(models.Model):
    """Seller information """

    user = models.OneToOneField(BasicUserMod, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.user.is_staff = True
        self.user.save()

        super(Seller, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class House(models.Model):
    """House information  """

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    about = models.TextField()
    street = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    district = models.CharField(max_length=80)
    lat = models.CharField(max_length=40, blank=True, null=True, default=None)
    lng = models.CharField(max_length=40, blank=True, null=True, default=None)
    rent = models.IntegerField()

    def geocoder(self):
        address = f" {self.street},{self.district},{self.city} "
        g = geocoder.google(address)
        return [g.lat, g.lng]

    def update_geocode(self):
        try:
            self.lat, self.lng = self.geocoder()
        except:
            self.lat, self.lng = [None, None]

    def save(self, *args, **kwargs):
        self.update_geocode()
        super(House, self).save(*args, **kwargs)


class Image(models.Model):
    """Image upload to folder uploads """

    image_file = models.ImageField(upload_to="uploads/", blank=True, null=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.house.title + " Image"


class Customer(models.Model):
    """Customer information"""

    user = models.OneToOneField(BasicUserMod, on_delete=models.CASCADE)
    liked_house = models.ManyToManyField(House)

    def __str__(self):
        return self.user.username
