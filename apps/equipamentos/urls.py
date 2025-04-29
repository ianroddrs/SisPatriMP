from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipamentos, name='equipamentos'),
    path('inserir_equipamento', views.inserir_equipamento, name='inserir_equipamento'),
]