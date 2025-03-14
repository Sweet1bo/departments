from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Настройка маршрутов API
router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)

# Пространство имен для шаблонов
app_name = 'departments'

urlpatterns = [
    # Маршруты для шаблонов
    path('', views.index, name='index'),
    path('department/<int:department_id>/', views.department_detail, name='department_detail'),

    # Маршруты для API
    path('api/', include(router.urls)),
]