from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from . models import Member

User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(max_length=254, required=True)
    contact_number = forms.CharField(max_length=10, required=True)
    password1 = forms.CharField(max_length=35, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=35, required=True, widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'contact_number', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email ID'
        self.fields['contact_number'].label = 'Contact Number'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        number = cleaned_data.get("contact_number")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        if Member.objects.filter(contact_number=number).exists():
            raise forms.ValidationError("Phone number already exists in our records")
        



