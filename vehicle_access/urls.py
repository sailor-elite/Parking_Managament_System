from django.urls import path
from . import views
from .views import vehicle_access_api, vehicle_access_web

app_name = 'vehicle_access'

urlpatterns = [
    path('api/vehicle-access/', vehicle_access_api, name='vehicle_access_api'),
    path('vehicle-access/', vehicle_access_web, name='search_vehicle'),

]
