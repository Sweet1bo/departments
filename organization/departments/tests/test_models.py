import pytest
from django.core.exceptions import ValidationError
from departments.models import Department, Employee
from departments.tests.factories import DepartmentFactory, EmployeeFactory

pytestmark = pytest.mark.django_db  # Помечаем все тесты в файле как требующие доступ к БД


class TestDepartmentModel:
    """
    Тесты для модели Department
    """

    def test_create_department(self):
        """Проверяем создание отдела"""
        department = DepartmentFactory()
        assert Department.objects.count() == 1
        assert department.name
        assert department.parent is None

    def test_create_subdepartment(self):
        """Проверяем создание подотдела"""
        parent = DepartmentFactory()
        child = DepartmentFactory(parent=parent)

        assert child.parent == parent
        assert parent in child.get_ancestors()
        assert child in parent.get_descendants()

    def test_department_tree(self, department_tree):
        """Проверяем структуру дерева отделов"""
        root = department_tree['root']
        child1 = department_tree['child1']
        child2 = department_tree['child2']
        grandchild = department_tree['grandchild']

        # Проверяем связи
        assert child1.parent == root
        assert child2.parent == root
        assert grandchild.parent == child1

        # Проверяем методы MPTT
        assert list(root.get_children()) == [child1, child2]
        assert list(child1.get_children()) == [grandchild]
        assert list(child2.get_children()) == []

        assert grandchild in root.get_descendants()
        assert child1 in root.get_descendants()
        assert child2 in root.get_descendants()

        assert root in grandchild.get_ancestors()
        assert child1 in grandchild.get_ancestors()

    def test_department_str(self):
        """Проверяем строковое представление отдела"""
        department = DepartmentFactory(name="Тестовый отдел")
        assert str(department) == "Тестовый отдел"


class TestEmployeeModel:
    """
    Тесты для модели Employee
    """

    def test_create_employee(self):
        """Проверяем создание сотрудника"""
        employee = EmployeeFactory()

        assert Employee.objects.count() == 1
        assert employee.full_name
        assert employee.position
        assert employee.hire_date
        assert employee.salary > 0
        assert employee.department is not None

    def test_employee_department_relationship(self, department_with_employees):
        """Проверяем связь сотрудника с отделом"""
        department = department_with_employees['department']
        employees = department_with_employees['employees']

        assert department.employees.count() == 5

        for employee in employees:
            assert employee.department == department

    def test_employee_str(self):
        """Проверяем строковое представление сотрудника"""
        employee = EmployeeFactory(full_name="Иванов Иван Иванович")
        assert str(employee) == "Иванов Иван Иванович"

    def test_employee_with_invalid_salary(self):
        """Проверяем валидацию отрицательной зарплаты"""
        with pytest.raises(ValidationError):
            employee = EmployeeFactory(salary=-1000)
            employee.full_clean()