from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.

phone_validator = RegexValidator(regex=r'^[0-9]{10}$')

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(validators = [phone_validator], max_length=10)
    
