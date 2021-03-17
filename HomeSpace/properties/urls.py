from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'properties'

urlpatterns = [
    path('add', views.createPropertyView, name='add'),
    path('add_photos/<int:pk>', views.add_property_images, name='add-images'),
    path('add_photos/upload/<int:pk>', views.add_images, name='upload'),
    path('add_location/<int:pk>', views.add_location, name="add-location"),  
    path('ajax_add_location/<int:pk>', views.ajax_add_location, name='ajax-add-location'),
    path('my', views.my_properties, name="my"),
    path('search', views.search_property, name="search"),
    path('view/<int:pk>', views.view_property, name="view"),
    path('ajax_shortlist_property/<int:pk>', views.shortlist_property, name="shortlist"),
    path('shortlisted', views.shortlisted_properties, name="shortlisted"),
    path('ajax_remove_shortlisted/<int:pk>', views.remove_shortlisted, name="ajax_remove_shortlisted"),
    path('ajax_load_localities/<int:pk>', views.load_localities, name="ajax_load_localities"),
]



