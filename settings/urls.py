from django.urls import path, include

from .view_root import api_root

urlpatterns = [
    path('', api_root),
    path('api/', include('currency.urls')),
    ]
