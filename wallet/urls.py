from django.urls import path

from . import views

urlpatterns = [
    path('connect-wallet', views.connect_wallet, name='connect_wallet')
]