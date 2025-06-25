from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('equipamentos/', include('apps.equipamentos.urls')),
    path('localidades/', include('apps.localidades.urls')),
    path('movimentacao/', include('apps.movimentacao.urls')),
    path('admin/', admin.site.urls),
    # Nova URL para a API de dados do dashboard
    path('api/dashboard_charts/', views.get_dashboard_chart_data, name='api_dashboard_charts'),
]
