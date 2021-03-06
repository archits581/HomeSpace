from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import PropertyDescriptionForm, PropertyImagesForm
from .models import PropertyDescription, PropertyImage, Location, Locality, City, Shortlisted
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from .filters import PropertyFilters
from accounts.models import Member


# Create your views here.

#Utility dictionary to store coordinates of cities in the database. Add coordinates of new city when the city is added to the database
coords = {
          "Mumbai": [19.0760, 72.8777],
          "Delhi": [28.7041, 77.1025],
          "Bangalore": [12.9716, 77.5946], 
          "Pune": [18.5204, 73.8567],
          "Hyderabad": [17.3850, 78.4867],
          "Chennai": [13.0827, 80.2707],
        }

User = get_user_model()

@login_required()
def createPropertyView(request):
    cities = City.objects.all()
    if request.method == 'POST':
        errors = []
        apartment_name = request.POST["apartment_number"];
        building_name = request.POST["building"];
        description = request.POST["description"];
        rent = int(request.POST["rent"]);
        deposit = int(request.POST["deposit"]);
        bedrooms = int(request.POST["bhk"]);

        #SERVER SIDE VALIDATION:
        if len(apartment_name) < 1:
            errors.append("Invalid apartment number. Apartment nunber should be at least 2 characters");
        if len(building_name) < 7:
            errors.append("Invalid building/society name. It should be at least 7 characters");
        if len(description) < 30:
            errors.append("Please add more information in the description section");
        if rent<2000 or rent>100000:
            errors.append("Rent cannot be more than 100000 or less than 2000 per month");
        if deposit<1000 or deposit>1000000:
            errors.append("Deposit cannot be more than 100000 or less than 1000 per month");
        if bedrooms<1 or bedrooms>7:
            errors.append("Cannot have more than 7 bedrooms or less than 1 bedroom");
        
        if len(errors) > 0:
            return render(request, 'properties/add.html', {'cities': cities, "errors": errors});

        form = PropertyDescriptionForm(request.POST)
        if form.is_valid():
            owner = get_object_or_404(User, pk=request.user.pk)
            property_object = form.save(commit=False)
            property_object.user=owner
            property_object.save()
            pk = property_object.pk
            return HttpResponseRedirect(reverse('properties:add-images', args=(pk,)))
    else:
        pass
    return render(request, 'properties/add.html', {'cities': cities, "errors": []});

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
    try:
        property_object = PropertyDescription.objects.get(pk=pk)
        if property_object.propertyimage_set.count() != 0:
            return HttpResponse('You have already uploaded images')
    except PropertyDescription.DoesNotExist:
        raise Http404('Could not find the page you were looking for')
    return render(request, 'properties/add_photos.html', {'pk': pk})


@login_required()
def add_location(request, pk):
    try:
        property_object = PropertyDescription.objects.get(pk=pk)
    except PropertyDescription.DoesNotExist:
        raise Http404('Page not found')
    lat = 0
    long = 0

    if hasattr(property_object, 'location'):
        return HttpResponse('You have already selected a location')
    city = property_object.city.name
    if city == "Mumbai":
        lat = coords[city][0]
        long = coords[city][1]
    return render(request, 'properties/add_location.html', {'primary_key':pk, 'center_lat': lat, 'center_long': long})


@login_required()
def ajax_add_location(request, pk):
    try:
        property_object = PropertyDescription.objects.get(pk=pk)
    except PropertyDescription.DoesNotExist:
        return JsonResponse({"error":"some error occured"}, status=400)
    if request.is_ajax and request.method == "POST":
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location_object = Location(property=property_object, lat=latitude, long=longitude)
        location_object.save()
        return JsonResponse({"message": "success"}, status=200)
    
    return JsonResponse({"error":"some error occured"}, status=400)


@login_required()
def my_properties(request):
    properties = PropertyDescription.objects.all().filter(user=request.user)
    context = {}
    context['properties'] = properties
    return render(request, 'properties/my.html', context)


def search_property(request):    
    context = {}
    context['cities'] = City.objects.all()
    context['localities'] = Locality.objects.all()

    lat = 0;
    long = 0;
    if not request.GET:
        return render(request, 'properties/search.html', context)
    else:
        if request.GET['tenant_type'] != 'Any':
            context['filter'] = PropertyFilters(request.GET, queryset=PropertyDescription.objects.all().filter(tenant_type=request.GET['tenant_type'], city=City.objects.get(pk=request.GET["city"]), locality=Locality.objects.get(pk=request.GET["locality"]) ))
        else:
            context['filter'] = PropertyFilters(request.GET, queryset=PropertyDescription.objects.all().filter(city=City.objects.get(pk=request.GET["city"]), locality=Locality.objects.get(pk=request.GET["locality"]) ))
        city_value = City.objects.get(pk=request.GET["city"]).name
        lat = coords[city_value][0];
        long = coords[city_value][1];
        context['lat'] = lat;
        context['long'] = long;
        context['query_set'] = []

        prop_objects = context['filter']
        for i in range(0, len(context['filter'].qs)):
            current = prop_objects.qs[i]
            print(current)
            if current.propertyimage_set.count() != 0 and (not Shortlisted.objects.filter(user=request.user, property=current).exists()) and hasattr(context['filter'].qs[i], 'location'):
                context['query_set'].append(context['filter'].qs[i])
        print(context)
    return render(request, 'properties/search.html', context)


def view_property(request, pk):
    try:
        property_object = PropertyDescription.objects.get(pk=pk)
    except PropertyDescription.DoesNotExist:
        raise Http404('Could not find what you were looking for')
    context = {};
    context['owner'] = property_object.user
    context['phone_number'] = context['owner'].member
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
    try:
        property_object = PropertyDescription.objects.get(pk=pk)
    except PropertyDescription.DoesNotExist:
        return JsonResponse({"error":"some error occured"}, status=400)
    if request.is_ajax and request.method == "POST":
        object = Shortlisted(user=request.user, property=property_object)
        object.save()
        # print('done\n\ndone')
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



#Utility function to provide localities for selected city in dependent dropdowns
def load_localities(request, pk):
    city_object = City.objects.get(pk=pk)
    context = {};
    if request.is_ajax and request.method == "GET":
        localities = Locality.objects.filter(city=city_object).order_by('name')
        context['localities'] = localities
        print('\nhello\n')
        return render(request, 'properties/city_dropdown.html', context)
    return JsonResponse({"error":"some error occured"}, status=400)
