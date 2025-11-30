from django.contrib import admin
from django.urls import path, include
from accounts.views import home  # IMPORTA LA VISTA

urlpatterns = [
    path('', home, name='home'),  # 👈 ESTA ES LA RUTA PRINCIPAL
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('tasks/', include('tasks.urls')),
]
