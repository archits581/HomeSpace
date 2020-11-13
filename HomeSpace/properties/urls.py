from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'properties'

urlpatterns = [
    path('add/', views.createPropertyView, name='add')
]
