import pytest
from rest_framework import status

from departments.tests.factories import DepartmentFactory, EmployeeFactory

pytestmark = pytest.mark.django_db


class TestDepartmentAPI:
    """
    Тесты для API отделов
    """

    def test_departments_list(self, api_client, multiple_departments):
        """Проверяем API получения списка отделов"""
        # Отправляем GET-запрос к API
        url = '/api/departments/'
        response = api_client.get(url)

        # Проверяем успешный ответ
        assert response.status_code == status.HTTP_200_OK

        # Проверяем данные ответа
        assert 'count' in response.data
        assert response.data['count'] == 3
        assert len(response.data['results']) == 3

    def test_department_detail(self, api_client, department_with_employees):
        """Проверяем API получения информации об отделе"""
        department = department_with_employees['department']

        # Отправляем GET-запрос к API
        url = f'/api/departments/{department.id}/'
        response = api_client.get(url)

        # Проверяем успешный ответ и данные
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == department.id
        assert response.data['name'] == department.name

        # Проверяем, что в ответе есть вложенные сотрудники
        assert 'employees' in response.data
        assert len(response.data['employees']) == 5

    def test_department_root(self, api_client, department_tree):
        """Проверяем API получения корневых отделов"""
        # Отправляем GET-запрос к API
        url = '/api/departments/root/'
        response = api_client.get(url)

        # Проверяем успешный ответ
        assert response.status_code == status.HTTP_200_OK

        # В дереве есть только один корневой отдел
        assert len(response.data) == 1
        assert response.data[0]['name'] == department_tree['root'].name

    def test_nonexistent_department(self, api_client):
        """Проверяем запрос к API для несуществующего отдела"""
        # Отправляем GET-запрос к API для несуществующего отдела
        url = '/api/departments/9999/'
        response = api_client.get(url)

        # Проверяем, что возвращается 404 Not Found
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestEmployeeAPI:
    """
    Тесты для API сотрудников
    """

    def test_employees_list(self, api_client, department_with_employees):
        """Проверяем API получения списка сотрудников"""
        # Отправляем GET-запрос к API
        url = '/api/employees/'
        response = api_client.get(url)

        # Проверяем успешный ответ
        assert response.status_code == status.HTTP_200_OK

        # Проверяем данные ответа
        assert 'count' in response.data
        assert response.data['count'] == 5
        assert len(response.data['results']) == 5

    def test_employee_detail(self, api_client, department_with_employees):
        """Проверяем API получения информации о сотруднике"""
        employee = department_with_employees['employees'][0]

        # Отправляем GET-запрос к API
        url = f'/api/employees/{employee.id}/'
        response = api_client.get(url)

        # Проверяем успешный ответ и данные
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == employee.id
        assert response.data['full_name'] == employee.full_name
        assert response.data['department'] == employee.department.id

    def test_filter_employees_by_department(self, api_client, department_with_employees):
        """Проверяем фильтрацию сотрудников по отделу"""
        department = department_with_employees['department']

        # Создаем дополнительный отдел с сотрудниками
        another_dept = DepartmentFactory()
        [EmployeeFactory(department=another_dept) for _ in range(3)]

        # Отправляем GET-запрос к API с фильтром по отделу
        url = f'/api/employees/?department={department.id}'
        response = api_client.get(url)

        # Проверяем успешный ответ
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что вернулись только сотрудники нужного отдела
        assert response.data['count'] == 5
        for employee in response.data['results']:
            assert employee['department'] == department.id