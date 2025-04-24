from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/datalists', views.api_datalists, name='api_datalists'),
]