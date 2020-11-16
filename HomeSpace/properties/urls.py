from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'properties'

urlpatterns = [
    path('add/', views.createPropertyView, name='add'),
    path('add_photos/<int:pk>', views.add_property_photos, name='add-photos'),
    path('add_photos/image_upload/<int:pk>', views.add_property_photos_util, name='add-photos-util'),
    path('add_cover_photo/<int:pk>', views.add_cover_photo, name='add-cover-photo'),
]
