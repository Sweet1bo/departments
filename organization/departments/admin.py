from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    """
    Административный интерфейс для модели Department с поддержкой MPTT
    """
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    mptt_level_indent = 20


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Employee
    """
    list_display = ('full_name', 'position', 'hire_date', 'salary', 'department')
    list_filter = ('department', 'position', 'hire_date')
    search_fields = ('full_name', 'position')
    date_hierarchy = 'hire_date'
    autocomplete_fields = ('department',)