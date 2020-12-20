from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyDescriptionForm, PropertyImagesForm
from .models import PropertyDescription, PropertyImage
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect

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
            property_object.save()
            pk = property_object.pk
            return HttpResponseRedirect(reverse('properties:add-images', args=(pk,)))
    else:
        form = PropertyDescriptionForm()
    return render(request, 'properties/add.html', {'form': form})

def homePage(request):
    return render(request, 'base.html', {})

@login_required()
def add_property_images(request, pk):
    if request.method == "POST":
        form = PropertyImagesForm(request.POST, request.FILES)   
        if form.is_valid():
            try:
                print("testing");
                image = form.save(commit = False)
                property_object = PropertyDescription.objects.get(pk=pk)
                image.property = property_object
                image.save()
                return HttpResponseRedirect(reverse('properties:add-images', args=(pk,)))
            except PropertyDescription.DoesNotExist:
                raise Http404('Property does not exist')
    else:
        form = PropertyImagesForm()
    return render(request, 'properties/add_photos.html', {'form': form})


@login_required()
def add_location(request, pk):
    return render(request, 'properties/add_location.html', {})
