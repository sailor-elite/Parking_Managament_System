from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import CustomTokenObtainPairView

app_name = "users"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
