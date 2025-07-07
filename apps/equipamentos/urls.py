from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipamentos, name='equipamentos'),
    path('create_equipamento/', views.create_equipamento, name='create_equipamento'),
    path('update_equipamento/<int:pk>/', views.update_equipamento, name='update_equipamento'),
    path('delete_equipamento/<int:pk>/', views.delete_equipamento, name='delete_equipamento'),

    path('api/locais-por-cidade/', views.get_locais_por_cidade, name='api_locais_por_cidade'),
    path('api/tipos-equipamento/', views.get_tipos_equipamento, name='api_tipos_equipamento'),
    path('api/fabricantes/', views.get_fabricantes, name='api_fabricantes'),
]
