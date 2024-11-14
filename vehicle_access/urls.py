from django.urls import path
from . import views

app_name = 'vehicle_access'

urlpatterns = [
    path('search/', views.search_vehicle, name='search_vehicle'),
]
