from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import PropertyDescription, PropertyImage
from PIL import Image
from django.core.files import File

User = get_user_model()

class PropertyDescriptionForm(forms.ModelForm):
    class Meta:
        model = PropertyDescription
        exclude = ['user']
    

class PropertyImagesForm(forms.ModelForm):
    
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = PropertyImage
        exclude = ['property']
    
    