from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'properties'

urlpatterns = [
    path('add/', views.createPropertyView, name='add'),
    path('add_photos/<int:pk>', views.add_property_images, name='add-images'),
    path('add_location/<int:pk>', views.add_location, name="add-location"),  
    path('ajax_add_location/<int:pk>', views.ajax_add_location, name='ajax-add-location'),
    path('my', views.my_properties, name="my"),
    path('search', views.search_property, name="search"),
]
