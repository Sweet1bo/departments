import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta

from departments.models import Department, Employee


class DepartmentFactory(DjangoModelFactory):
    """
    Фабрика для создания тестовых отделов
    """

    class Meta:
        model = Department

    name = factory.Sequence(lambda n: f'Тестовый отдел {n}')

    # Создает отдел без родителя по умолчанию
    # Для создания подотдела нужно указать parent=some_department

    @factory.post_generation
    def with_employees(self, create, extracted, **kwargs):
        """
        Создает сотрудников для отдела
        Использование: DepartmentFactory(with_employees=5)
        """
        if not create:
            return

        if extracted:
            count = extracted
            for _ in range(count):
                EmployeeFactory(department=self)


class EmployeeFactory(DjangoModelFactory):
    """
    Фабрика для создания тестовых сотрудников
    """

    class Meta:
        model = Employee

    full_name = factory.Faker('name', locale='ru_RU')
    position = factory.Faker('job', locale='ru_RU')
    hire_date = factory.LazyFunction(lambda: (timezone.now() - timedelta(days=random.randint(1, 3650))).date())
    salary = factory.LazyFunction(lambda: Decimal(random.randrange(30000, 150000, 5000)))

    # Создаем новый отдел для каждого сотрудника если не указан явно
    department = factory.SubFactory(DepartmentFactory)