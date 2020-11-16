from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyDescriptionForm
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
            return HttpResponseRedirect(reverse('properties:add-photos', args=(pk,)))
    else:
        form = PropertyDescriptionForm()
    return render(request, 'properties/add.html', {'form': form})

def homePage(request):
    return render(request, 'base.html', {})

def add_property_photos(request, pk):
    return render(request, 'properties/add_photos.html', {'pk': pk})

def add_property_photos_util(request, pk):
    if request.method == 'POST':
        image_file = request.FILES.get('file')
        try:
            property_object = PropertyDescription.objects.get(pk=pk)
            PropertyImage.objects.create(image=image_file, property=property_object)
        except PropertyDescription.DoesNotExist:
            raise Http404('Property does not exist')
        return HttpResponse('')
    return JsonResponse({'post': 'false'})
