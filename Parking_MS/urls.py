from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('stats', views.stats, name='stats'),
    path('users/', include('users.urls')),
    path('vehicles/', include('vehicles.urls'), name='vehicles'),
    path('transactions/', include('transactions.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
