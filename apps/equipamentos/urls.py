from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipamentos, name='equipamentos'),
    path('create_equipamento', views.create_equipamento, name='create_equipamento'),
]