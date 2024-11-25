from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('stats', views.stats, name='stats'),
    path('users/', include('users.urls')),
    path('vehicles/', include('vehicles.urls'), name='vehicles'),
    path('transactions/', include('transactions.urls')),
    path('vehicle_access/', include('vehicle_access.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
