from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import PropertyDescriptionForm, PropertyImagesForm
from .models import PropertyDescription, PropertyImage, Location, Locality, City, Shortlisted
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
        cities = City.objects.all();
    return render(request, 'properties/add.html', {'form': form, 'cities': cities})

def homePage(request):
    return render(request, 'properties/landing.html', {})


@login_required
def add_images(request, pk):
    if request.method == "POST":
        try:
            my_file = request.FILES.get('file')
            property_object = PropertyDescription.objects.get(pk = pk)
            PropertyImage.objects.create(image=my_file, property=property_object)
        except PropertyDescription.DoesNotExist:
            raise Http404('Page Not Found')
        return HttpResponse('')
    return JsonResponse({'post': false})

@login_required()
def add_property_images(request, pk):
    # if request.method == "POST":
    #     form = PropertyImagesForm(request.POST, request.FILES)   
    #     if form.is_valid():
    #         try:
    #             print("testing");
    #             image = form.save(commit = False)
    #             property_object = PropertyDescription.objects.get(pk=pk)
    #             image.property = property_object
    #             image.save()
    #             return HttpResponseRedirect(reverse('properties:add-images', args=(pk,)))
    #         except PropertyDescription.DoesNotExist:
    #             raise Http404('Property does not exist')
    # else:
    #     form = PropertyImagesForm()
    try:
        property_object = PropertyDescription.objects.get(pk=pk)
        if property_object.propertyimage_set.count() != 0:
            return HttpResponse('You have already uploaded images')
    except PropertyDescription.DoesNotExist:
        raise Http404('Could not find the page you were looking for')
    return render(request, 'properties/add_photos.html', {'pk': pk})


@login_required()
def add_location(request, pk):
    property_object = PropertyDescription.objects.get(pk=pk)
    lat = 0
    long = 0

    if hasattr(property_object, 'location'):
        return HttpResponse('You have already selected a location')
    city = property_object.city.name
    if city == "Mumbai":
        lat = 19.0760
        long = 72.8777
    return render(request, 'properties/add_location.html', {'primary_key':pk, 'center_lat': lat, 'center_long': long})


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

    lat = 0;
    long = 0;

    if not request.GET:
        return render(request, 'properties/search.html', context)
    else:
        context['filter'] = PropertyFilters(request.GET, queryset=PropertyDescription.objects.all())
        if request.GET['locality'] == 'Andheri' or request.GET['locality'] == 'andheri':
            lat = 19.1136;
            long = 72.8697;

        context['lat'] = lat;
        context['long'] = long;
        context['query_set'] = []

        for i in range(0, len(context['filter'].qs)):
            if context['filter'].qs[i].propertyimage_set.count() != 0 and hasattr(context['filter'].qs[i], 'location'):
                context['query_set'].append(context['filter'].qs[i])
                # print(context['query_set'][0].propertyimage_set.all())
                # print(context['filter'])
                # for i in range (len(context['filter'].qs)):
                # print(context['filter'].qs[i])
                # print(context['filter'].qs[i].propertyimage_set.all()[0])
        print(context)
    return render(request, 'properties/search.html', context)


def view_property(request, pk):
    property_object = PropertyDescription.objects.get(pk=pk)
    context = {};
    context['property'] = property_object;
    lat = property_object.location.lat
    long = property_object.location.long
    context['lat'] = lat
    context['long'] = long
    logged_in = False;
    has_shortlisted = False;
    if request.user.is_authenticated:
        logged_in = True;
        user_object = request.user;
        try:
            entry = Shortlisted.objects.get(property=property_object, user=user_object)
            has_shortlisted = True;
        except Shortlisted.DoesNotExist:
            has_shortlisted = False
    context['shortlisted'] = has_shortlisted
    return render(request, 'properties/view.html', context)


@login_required
def shortlist_property(request, pk):
    property_object = PropertyDescription.objects.get(pk=pk)
    if request.is_ajax and request.method == "POST":
        object = Shortlisted(user=request.user, property=property_object)
        object.save()
        print('done\n\ndone')
        return JsonResponse({"message": "success"}, status=200)
    return JsonResponse({"error":"some error occured"}, status=400)


@login_required
def shortlisted_properties(request):
    properties = Shortlisted.objects.filter(user=request.user).values_list('property', flat=True)
    context = {}
    list = []
    for p in properties:
        list.append(PropertyDescription.objects.get(pk=p))
    context['query_set'] = list
    return render(request, 'properties/shortlisted.html', context);

@login_required
def remove_shortlisted(request, pk):
    property_object = PropertyDescription.objects.get(pk=pk)
    user_object = request.user
    if request.is_ajax and request.method == "POST":
        Shortlisted.objects.get(property=property_object, user=user_object).delete();
        return JsonResponse({"message": "success"}, status=200)
    return JsonResponse({"error":"some error occured"}, status=400)


def load_localities(request, pk):
    city_object = City.objects.get(pk=pk)
    context = {};
    if request.is_ajax and request.method == "GET":
        localities = Locality.objects.filter(city=city_object).order_by('name')
        context['localities'] = localities
        print('\nhello\n')
        return render(request, 'properties/city_dropdown.html', context)
    return JsonResponse({"error":"some error occured"}, status=400)
