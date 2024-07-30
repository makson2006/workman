from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Додає стандартні маршрути для аутентифікації
    path('projects/', include('projects.urls')),
]
