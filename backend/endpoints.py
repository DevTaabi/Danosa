from django.urls import path

from . import api

urlpatterns = [
    path('signup/', api.signup),
    path('login/', api.login),
    path('userbyid/<userid>/', api.userbyid),
    path('user_update/<userid>/', api.user_update),
    path('reset_password/', api.reset_password),
    path('logout/', api.logout),
    path('add_products/', api.add_products),
    path('getproducts/', api.getproducts),
]