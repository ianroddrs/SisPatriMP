from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/localidades', views.api_localidades, name='api_localidades'),
]