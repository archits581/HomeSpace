from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyDescriptionForm, PropertyImagesForm
from .models import PropertyDescription, PropertyImage, Location, Locality, City
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from .filters import PropertyFilters

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
    return render(request, 'properties/landing.html', {})

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
    property_object = PropertyDescription.objects.get(pk=pk)
    if not property_object.location:
        return render(request, 'properties/add_location.html', {'primary_key':pk})
    return HttpResponse('You have already selected a location')

@login_required()
def ajax_add_location(request, pk):
    property_object = PropertyDescription.objects.get(pk=pk)
    if request.is_ajax and request.method == "POST":
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location_object = Location(property=property_object, lat=latitude, long=longitude)
        location_object.save()
        return JsonResponse({"message": "success"}, status=200)
    
    return JsonResponse({"error":"some error occured"}, status=400)


@login_required()
def my_properties(request):
    return HttpResponse("successful")



def search_property(request):
    
    context = {}
    context['localities'] = Locality.objects.all()

    if not request.GET:
        return render(request, 'properties/search.html', context)
    else:
        context['filter'] = PropertyFilters(request.GET, queryset=PropertyDescription.objects.all())
        context['query_set'] = []

        for i in range(0, len(context['filter'].qs)):
            if context['filter'].qs[i].propertyimage_set.count() != 0:
                context['query_set'].append(context['filter'].qs[i])
                # print(context['query_set'][0].propertyimage_set.all())
                # print(context['filter'])
                # for i in range (len(context['filter'].qs)):
                # print(context['filter'].qs[i])
                # print(context['filter'].qs[i].propertyimage_set.all()[0])
    return render(request, 'properties/search.html', context)
