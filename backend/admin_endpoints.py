from django.urls import path

from . import admin_api
urlpatterns = [
    path('index/', admin_api.index),
    path('login/', admin_api.login),
    path('add_user/', admin_api.add_user),
    path('all_users/', admin_api.all_users),
    path('userbyid/<uid>', admin_api.userbyid),
    path('update_user/<uid>', admin_api.update_user),
    path('del_user/<uid>', admin_api.del_user),
]