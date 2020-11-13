from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyDescriptionForm
from .models import PropertyDescription
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.

User = get_user_model()

@login_required()
def createPropertyView(request):
    if request.method == 'POST':
        form = PropertyDescriptionForm(request.POST)
        if form.is_valid():
            owner = get_object_or_404(User, pk=request.user.pk)
            property_object = form.save(commit=False)
            property_object.user=owner
            return redirect('properties:all')
    else:
        form = PropertyDescriptionForm()
    return render(request, 'properties/add.html', {'form': form})

def homePage(request):
    return render(request, 'base.html', {})

