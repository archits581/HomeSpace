import django_filters
from .models import PropertyDescription

class PropertyFilters(django_filters.FilterSet):
    class Meta:
        model = PropertyDescription
        fields = {
                  'rent': ['lt'], 
                  'bhk': ['exact'], 
                  'tenant_type': ['exact'], 
                  'furnished':['exact'], 
                  'locality':['exact'], 
                  }
