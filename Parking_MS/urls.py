from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('stats', views.stats, name='stats'),
    path('users/', include('users.urls')),
    path('vehicles/', include('vehicles.urls'), name='vehicles'),
    path('transactions/', include('transactions.urls')),
]
