from django.contrib import admin
from .models import City, Locality, PropertyDescription, PropertyImage, Location, Shortlisted

# Register your models here.
admin.site.register(City)
admin.site.register(Locality)
admin.site.register(PropertyDescription)
admin.site.register(PropertyImage)
admin.site.register(Location)
admin.site.register(Shortlisted)
