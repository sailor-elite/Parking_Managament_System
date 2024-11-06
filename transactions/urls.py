from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path('', views.transactions_view, name='transactions'),
    path('add/', views.add_transaction, name='add_transaction'),
]
