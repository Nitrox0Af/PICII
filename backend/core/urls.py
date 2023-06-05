from django.urls import path

from .views import index, owner, guest, encoding, guest_json, owner_json, telegram, telegram_bot, create_owner, create_guest

urlpatterns = [
    path('', index, name='index'),
    path('owner/', owner, name='owner'),
    path('guest/', guest, name='guest'),
    path('encoding/<str:filename>/', encoding, name='encoding'),
    path('guest/json/<str:cpf>/', guest_json, name='guest-json'),
    path('owner/json/<str:cpf>/', owner_json, name='owner-json'),
    path('telegram/', telegram, name='telegram'),
    path('telegram/bot/', telegram_bot, name='telegram-bot'),
    path('create/owner/', create_owner, name='create-owner'),
    path('create/guest/', create_guest, name='create-guest'),
]