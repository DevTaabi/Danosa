from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', include('backend.endpoints')),
    path('api/admin/', include('backend.admin_endpoints')),
    path('fcm/', include('fcm.urls')),
]