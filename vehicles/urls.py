from django.urls import path
from . import views

app_name = "vehicles"

urlpatterns = [
    path("", views.vehicles_view, name="vehicles")
]
