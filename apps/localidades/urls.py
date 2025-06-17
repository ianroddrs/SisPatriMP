from django.urls import path
from .views import LocalidadesView, local_update, local_delete

urlpatterns = [
    # Rota principal para listar e criar localidades (usando a Class-Based View)
    path('', LocalidadesView.as_view(), name='localidades'),
    
    # Rota para atualizar um local específico
    # Ex: /localidades/update/5/
    path('update/<int:pk>/', local_update, name='local_update'),
    
    # Rota para deletar um local específico
    # Ex: /localidades/delete/5/
    path('delete/<int:pk>/', local_delete, name='local_delete'),
]
