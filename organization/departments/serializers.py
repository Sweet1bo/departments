from rest_framework import serializers
from .models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели сотрудника"""

    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'hire_date', 'salary', 'department']


class DepartmentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели отдела"""

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'level']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор отдела с вложенной информацией"""

    employees = EmployeeSerializer(source='employees.all', many=True, read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'level', 'employees', 'children']

    def get_children(self, obj):
        """Получаем дочерние отделы"""
        return DepartmentSerializer(obj.get_children(), many=True).data