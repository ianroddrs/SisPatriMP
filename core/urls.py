from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('equipamentos/', include('apps.equipamentos.urls')),
    path('localidades/', include('apps.localidades.urls')),
    path('movimentacao/', include('apps.movimentacao.urls')),
    path('admin/', admin.site.urls),
]