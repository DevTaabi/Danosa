from django.urls import path

from . import api

urlpatterns = [
    path('signup/', api.signup),
    path('login/', api.login),
    path('viewusers/', api.viewusers),
    path('userbyid/<userid>/', api.userbyid),
    path('user_update/<userid>/', api.user_update),
    path('del_user/<userid>/', api.del_user),
    path('add_products/', api.add_products),
    path('getproducts/', api.getproducts),

]