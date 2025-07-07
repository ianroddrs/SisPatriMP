from django.urls import path
from .views import LocalidadesView, local_update, local_delete

urlpatterns = [
    path('', LocalidadesView.as_view(), name='localidades'),
    
    path('update/<int:pk>/', local_update, name='local_update'),
    
    path('delete/<int:pk>/', local_delete, name='local_delete'),
]
