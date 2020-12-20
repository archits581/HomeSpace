from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'properties'

urlpatterns = [
    path('add/', views.createPropertyView, name='add'),
    path('add_photos/<int:pk>', views.add_property_images, name='add-images'),
]
