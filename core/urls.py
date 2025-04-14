from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls')),
    path('equipamentos/', include('apps.equipamentos.urls')),
    path('localidades/', include('apps.localidades.urls')),
    path('admin/', admin.site.urls),
]