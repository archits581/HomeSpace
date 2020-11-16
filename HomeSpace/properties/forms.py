from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import PropertyDescription, PropertyImage, CoverPhoto
from PIL import Image
from django.core.files import File

User = get_user_model()

class PropertyDescriptionForm(ModelForm):
    class Meta:
        model = PropertyDescription
        exclude = ['user']
    
    # def __init__(self, *args, **kwargs):


class CoverPhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = CoverPhoto
        fields = ('image', 'x', 'y', 'width', 'height', )
        exclude = ['property']

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo