from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Department, Employee
from .serializers import DepartmentSerializer, DepartmentDetailSerializer, EmployeeSerializer


# --------- Django Template Views ---------

def index(request):
    """
    Главная страница с деревом отделов
    """
    # Получаем только корневые отделы (без родителей)
    root_departments = Department.objects.filter(parent=None).prefetch_related('employees')

    return render(request, 'departments/index.html', {
        'departments': root_departments
    })


def department_detail(request, department_id):
    """
    Страница с детальной информацией об отделе и пагинацией сотрудников
    """
    department = get_object_or_404(Department, id=department_id)
    employees = Employee.objects.filter(department=department)

    # Пагинация для эффективной работы с большим количеством сотрудников
    paginator = Paginator(employees, 20)  # 20 сотрудников на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'departments/department_detail.html', {
        'department': department,
        'page_obj': page_obj
    })


# --------- REST API Views ---------

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для отделов.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def root(self, request):
        """
        Получение корневых отделов (без родителей)
        """
        root_departments = Department.objects.filter(parent=None)
        serializer = self.get_serializer(root_departments, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для сотрудников.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """
        Фильтрация сотрудников по отделу, если указан параметр department
        """
        queryset = Employee.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset