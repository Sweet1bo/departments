from django.core.management.base import BaseCommand
from django.utils import timezone
from departments.models import Department, Employee
import random
from faker import Faker
import decimal
from datetime import timedelta

fake = Faker('ru_RU')  # Используем русскую локализацию

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Заполнение базы данных...')
        
        # Создаем отделы (5 уровней, 25 отделов)
        self.create_departments()
        
        # Создаем сотрудников (50,000)
        self.create_employees()
        
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
    
    def create_departments(self):
        # Очищаем существующие данные
        Department.objects.all().delete()
        
        # Создаем отделы 1 уровня (5 отделов)
        level1_depts = []
        for i in range(5):
            dept = Department.objects.create(
                name=f"Отдел {i+1}"
            )
            level1_depts.append(dept)
            self.stdout.write(f'Создан отдел 1 уровня: {dept.name}')
        
        # Создаем отделы 2 уровня (10 отделов)
        level2_depts = []
        for i, parent in enumerate(level1_depts):
            for j in range(2):
                dept = Department.objects.create(
                    name=f"{parent.name} - Подотдел {j+1}",
                    parent=parent
                )
                level2_depts.append(dept)
                self.stdout.write(f'Создан отдел 2 уровня: {dept.name}')
        
        # Создаем отделы 3 уровня (5 отделов)
        level3_depts = []
        for i, parent in enumerate(level2_depts[:5]):
            dept = Department.objects.create(
                name=f"{parent.name} - Подотдел 1",
                parent=parent
            )
            level3_depts.append(dept)
            self.stdout.write(f'Создан отдел 3 уровня: {dept.name}')
        
        # Создаем отделы 4 уровня (3 отдела)
        level4_depts = []
        for i, parent in enumerate(level3_depts[:3]):
            dept = Department.objects.create(
                name=f"{parent.name} - Подотдел 1",
                parent=parent
            )
            level4_depts.append(dept)
            self.stdout.write(f'Создан отдел 4 уровня: {dept.name}')
        
        # Создаем отделы 5 уровня (2 отдела)
        for i, parent in enumerate(level4_depts[:2]):
            dept = Department.objects.create(
                name=f"{parent.name} - Подотдел 1",
                parent=parent
            )
            self.stdout.write(f'Создан отдел 5 уровня: {dept.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Создано {Department.objects.count()} отделов'))
    
    def create_employees(self):
        # Очищаем существующих сотрудников
        Employee.objects.all().delete()
        
        departments = list(Department.objects.all())
        positions = [
            'Менеджер', 'Разработчик', 'Дизайнер', 'Аналитик', 'HR специалист', 
            'Инженер по тестированию', 'Маркетолог', 'Менеджер по продажам', 
            'Бухгалтер', 'Администратор', 'Руководитель отдела', 'Технический писатель',
            'Системный администратор', 'Директор', 'Секретарь'
        ]
        
        # Пакетное создание для повышения производительности
        batch_size = 1000
        total_employees = 50000
        
        for i in range(0, total_employees, batch_size):
            batch_employees = []
            for j in range(min(batch_size, total_employees - i)):
                hire_date = fake.date_between(start_date='-10y', end_date='today')
                salary = decimal.Decimal(random.randrange(30000, 150000, 5000))
                
                employee = Employee(
                    full_name=fake.name(),
                    position=random.choice(positions),
                    hire_date=hire_date,
                    salary=salary,
                    department=random.choice(departments)
                )
                batch_employees.append(employee)
            
            Employee.objects.bulk_create(batch_employees)
            self.stdout.write(f'Создано {i + len(batch_employees)} сотрудников')
        
        self.stdout.write(self.style.SUCCESS(f'Создано {Employee.objects.count()} сотрудников'))
