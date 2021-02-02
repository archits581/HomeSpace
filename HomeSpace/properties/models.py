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
    name = models.CharField(blank=False, max_length=30, unique=True)
    
    def __str__(self):
        return self.name

class Locality(models.Model):
    name = models.CharField(blank=False, max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PropertyDescription(models.Model):
    apartment_number = models.CharField(blank=False, max_length=7)
    building = models.CharField(blank=False, max_length=255)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False)
    description = models.TextField(blank=False, max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rent = models.IntegerField(blank=False, validators=[MinValueValidator(2000), MaxValueValidator(100000)])
    negotiable = models.BooleanField(blank=False, default=True)
    tenant_type = models.CharField(max_length=30, choices=tenant_choices, blank=False)
    deposit = models.IntegerField(blank=False ,validators=[MinValueValidator(1000), MaxValueValidator(1000000)])
    furnished = models.CharField(blank=False, max_length=30, choices=furnished_choices)
    bhk = models.PositiveSmallIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(6)], default=1)
    club_house = models.BooleanField(blank=False, default=False)
    swimming_pool = models.BooleanField(blank=False, default=False)
    security = models.BooleanField(blank=False, default=False)
    gym = models.BooleanField(blank=False, default=False)
    lift = models.BooleanField(blank=False, default=False)
    play_area = models.BooleanField(blank=False, default=False)
    internet_services = models.BooleanField(blank=False, default=False)

class PropertyImage(models.Model):
    property = models.ForeignKey(PropertyDescription, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_image/')

class Location(models.Model):
    property = models.OneToOneField(PropertyDescription, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=22, decimal_places=16)
    long = models.DecimalField(max_digits=22, decimal_places=16)

class Shortlisted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(PropertyDescription, on_delete=models.CASCADE)

