from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "vehicles"

urlpatterns = [
    path("", views.vehicles_view, name="vehicles")
]
