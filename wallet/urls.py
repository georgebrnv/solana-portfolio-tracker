from django.urls import path

from . import views

urlpatterns = [
    path('wallet', views.add_wallet, name='add_wallet')
]