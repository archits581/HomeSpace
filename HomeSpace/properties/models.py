from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

User = get_user_model()

tenant_choices = [
    ('Bachelors', 'Bachelors'),
    ('Family Only', 'Family Only'),
    ('Any', 'Any')
]

furnished_choices = [
    ('Unfurnished', 'Unfurnished'),
    ('Semi furnished', 'Semi furnished'),
    ('Furnished', 'Unfurnished'),
]

class City(models.Model):
    name = models.CharField(blank=False, max_length=30)

class Locality(models.Model):
    name = models.CharField(blank=False, max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class PropertyDescription(models.Model):
    apartment_number = models.CharField(blank=False, max_length=7)
    building = models.CharField(blank=False, max_length=255)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.TextField(blank=False, max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_pic = models.ImageField(blank=False, upload_to='photos/cover')
    price = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(100000)])
    tenant_type = models.CharField(max_length=30, choices=tenant_choices)
    deposit = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(1000000)])
    furnished = models.CharField(max_length=30, choices=furnished_choices)
    club_house = models.BooleanField()
    swimming_pool = models.BooleanField()
    security = models.BooleanField()
    ac = models.BooleanField()
    gym = models.BooleanField()
    lift = models.BooleanField()
    play_area = models.BooleanField()
    internet_services = models.BooleanField()