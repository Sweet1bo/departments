from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Настройки для Swagger документации API
schema_view = get_schema_view(
    openapi.Info(
        title="Организационная структура API",
        default_version='v1',
        description="API для работы с отделами и сотрудниками",
        contact=openapi.Contact(email="admin@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('departments.urls')),

    # Документация API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Авторизация для API (browsable API)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]