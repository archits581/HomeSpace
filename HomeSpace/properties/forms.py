from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import PropertyDescription

User = get_user_model()

class PropertyDescriptionForm(ModelForm):
    class Meta:
        model = PropertyDescription
        exclude = ['user']
    
    # def __init__(self, *args, **kwargs):
        