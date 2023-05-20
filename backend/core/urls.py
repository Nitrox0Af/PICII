from django.urls import path

from .views import index, owner, guest

urlpatterns = [
    path('', index, name='index'),
    path('owner/', owner, name='owner'),
    path('guest/', guest, name='guest'),
]