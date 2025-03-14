import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from departments.tests.factories import DepartmentFactory, EmployeeFactory

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organization.settings')

django.setup()

@pytest.fixture
def api_client():
    """
    Фикстура для создания API клиента
    """
    return APIClient()


@pytest.fixture
def admin_user():
    """
    Фикстура для создания администратора
    """
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )
    return admin


@pytest.fixture
def authenticated_client(admin_user):
    """
    Фикстура для создания авторизованного API клиента
    """
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def department_tree():
    """
    Фикстура для создания дерева отделов:

    root_dept
        child_dept1
            grandchild_dept
        child_dept2
    """
    root_dept = DepartmentFactory()
    child_dept1 = DepartmentFactory(parent=root_dept)
    child_dept2 = DepartmentFactory(parent=root_dept)
    grandchild_dept = DepartmentFactory(parent=child_dept1)

    return {
        'root': root_dept,
        'child1': child_dept1,
        'child2': child_dept2,
        'grandchild': grandchild_dept
    }


@pytest.fixture
def department_with_employees():
    """
    Фикстура для создания отдела с несколькими сотрудниками
    """
    department = DepartmentFactory()
    employees = [EmployeeFactory(department=department) for _ in range(5)]

    return {
        'department': department,
        'employees': employees
    }


@pytest.fixture
def multiple_departments():
    """
    Фикстура для создания нескольких отделов верхнего уровня
    """
    departments = [DepartmentFactory() for _ in range(3)]
    return departments
