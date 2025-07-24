from django.urls import path
from . import views

urlpatterns = [
    path('', views.impressoras, name='impressoras'), 
    path('api/printers_status/', views.printers_status, name='printers_status'), 
]