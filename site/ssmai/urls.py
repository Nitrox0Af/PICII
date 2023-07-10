from django.urls import path

from .views import index, encoding, guest_json, owner_json, telegram, check_fingerprint, delete_fingerprint

urlpatterns = [
    path('', index, name='index'),
    path('encoding/<str:filename>/', encoding, name='encoding'),
    path('guest/json/<str:phone>/', guest_json, name='guest-json'),
    path('owner/json/<str:phone>/', owner_json, name='owner-json'),
    path('telegram/', telegram, name='telegram'),
    path('guest/fingerprint/check/<str:phone>/', check_fingerprint, name='check-fingerprint'),
    path('guest/fingerprint/delete/<str:phone>/', delete_fingerprint, name='delete-fingerprint')
]