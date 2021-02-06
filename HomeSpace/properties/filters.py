import django_filters
from .models import PropertyDescription

class PropertyFilters(django_filters.FilterSet):
    class Meta:
        model = PropertyDescription
        fields = {
                  'rent': ['lt', 'exact'], 
                  'bhk': ['exact'], 
                  'furnished':['exact'],
                  'city': ['exact'], 
                  'locality':['exact'], 
                  }
