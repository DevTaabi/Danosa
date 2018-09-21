from django.contrib import admin
from django.urls import include,path
from . import views
urlpatterns = [
    path('api/', include('backend.endpoints')),
    path('api/admin/', include('backend.admin_endpoints')),
]
