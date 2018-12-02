from django.urls import path

from . import admin_api
urlpatterns = [
    path('login/', admin_api.login),
    path('add_user/', admin_api.add_user),
    path('all_users/', admin_api.all_users),
    path('userbyid/<uid>', admin_api.userbyid),
    path('update_user/<uid>', admin_api.update_user),
    path('del_user/<uid>', admin_api.del_user),
    path('add_products/', admin_api.add_products),
    path('getproducts/', admin_api.getproducts),
    path('productbytype/<type>', admin_api.productbytype),
    path('productbyid/<type>/<id>', admin_api.productbyid),
    path('updateproduct/<typ>/<id>', admin_api.updateproduct),
    path('delproduct/<type>/<id>', admin_api.delproduct),
    path('all_quotes/', admin_api.all_quotes),
    path('del_quote/<userid>/<id>', admin_api.del_quote),
    path('update_note/<userid>/<id>', admin_api.update_note),
    path('quote_by_userid/<userid>/', admin_api.quote_by_userid),
    path('update_token/<userid>/', admin_api.update_token),
    path('sendnotify/', admin_api.sendnotify),
    path('sendnotify_to_all/', admin_api.sendnotify_to_all),
]