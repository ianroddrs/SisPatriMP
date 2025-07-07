from django.urls import path
from . import views

urlpatterns = [
    path('', views.movimentacoes, name='movimentacao'),
    path('perform_movimentacao/', views.perform_movimentacao, name='perform_movimentacao'),
    path('update_movimentacao/<int:pk>/', views.update_movimentacao, name='update_movimentacao'),
    path('delete_movimentacao/<int:pk>/', views.delete_movimentacao, name='delete_movimentacao'),

    path('api/movimentacao/equipamentos/', views.api_equipamentos_for_movimentacao, name='api_equipamentos_for_movimentacao'),
    path('api/movimentacao/locais/', views.api_locais_for_movimentacao, name='api_locais_for_movimentacao'),
]


