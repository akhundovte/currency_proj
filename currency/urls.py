from django.urls import path
from currency import views


urlpatterns = [
    path('currencies/', views.CurrencyList.as_view(), name='currency'),
    path('currency/<int:pk>/', views.CurrencyDetail.as_view(), name='currency-detail'),
    ]
