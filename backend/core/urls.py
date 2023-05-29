from django.urls import path

from .views import index, owner, guest, encoding, guest_json

urlpatterns = [
    path('', index, name='index'),
    path('owner/', owner, name='owner'),
    path('guest/', guest, name='guest'),
    path('encoding/<str:filename>/', encoding, name='encoding'),
    path('guest/json/<str:cpf>/', guest_json, name='guest-json')
]