from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    """
    Модель отдела с древовидной структурой (до 5 уровней)
    Используем MPTT для эффективной работы с деревом
    """
    name = models.CharField('Название', max_length=100)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительский отдел'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    Модель сотрудника с привязкой к отделу
    """
    full_name = models.CharField('ФИО', max_length=200)
    position = models.CharField('Должность', max_length=100)
    hire_date = models.DateField('Дата приема на работу')
    salary = models.DecimalField(
        'Размер заработной платы',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, message='Salary cannot be negative')]
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='Отдел'
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['hire_date']),
        ]

    def __str__(self):
        return self.full_name