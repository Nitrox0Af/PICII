from django.urls import path

from .views import index, guest, encoding, guest_json, owner_json, telegram, telegram_bot, create_guest

urlpatterns = [
    path('', index, name='index'),
    path('guest/', guest, name='guest'),
    path('encoding/<str:filename>/', encoding, name='encoding'),
    path('guest/json/<str:email>/', guest_json, name='guest-json'),
    path('owner/json/<str:email>/', owner_json, name='owner-json'),
    path('telegram/', telegram, name='telegram'),
    path('telegram/bot/', telegram_bot, name='telegram-bot'),
    path('create/guest/', create_guest, name='create-guest'),
]