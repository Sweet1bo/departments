# Тестовое задание - Организационная структура

Django-приложение для отображения древовидной структуры отделов компании со списком сотрудников. Поддерживает иерархию отделов до 5 уровней и содержит информацию о более чем 50 000 сотрудников.

## Технический стек

- Django 3.2+
- Python 3.8+
- PostgreSQL
- Bootstrap 5
- Django MPTT (Modified Preorder Tree Traversal) для эффективной работы с деревьями

## Функционал

- Древовидное представление отделов с возможностью сворачивания/разворачивания
- Отображение списка сотрудников отдела с пагинацией
- CRUD операции через административный интерфейс Django
- Генерация тестовых данных: 25 отделов в 5 уровнях иерархии и 50 000 сотрудников

## Установка и запуск

### Через Docker (рекомендуется)

1. Установите Docker и Docker Compose
2. Клонируйте репозиторий
3. Запустите приложение:
```bash
docker-compose up -d
```
4. Откройте приложение в браузере по адресу http://localhost:8000
5. Административный интерфейс доступен по адресу http://localhost:8000/admin 
   (логин: admin, пароль: admin)

### Обычная установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv venv
```
3. Активируйте виртуальное окружение:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
4. Установите зависимости: 
```bash
pip install -r requirements.txt
```
5. Настройте базу данных PostgreSQL
6. Обновите настройки базы данных в `organization/settings.py`
7. Примените миграции: 
```bash
python manage.py migrate
```
8. Заполните базу данных тестовыми данными: 
```bash
python manage.py populate_db
```
9. Создайте суперпользователя: 
```bash
python manage.py createsuperuser
```
10. Запустите сервер: 
```bash
python manage.py runserver
```
11. Откройте приложение в браузере по адресу http://localhost:8000

## Структура базы данных

- **Department**: Иерархическая структура отделов
  - name: Название отдела
  - parent: Родительский отдел (null для отделов верхнего уровня)

- **Employee**: Информация о сотрудниках
  - full_name: ФИО сотрудника
  - position: Должность
  - hire_date: Дата приема на работу
  - salary: Размер заработной платы
  - department: Внешний ключ на отдел

## Особенности производительности

- MPTT используется для эффективной работы с деревом отделов
- Пагинация реализована для отображения сотрудников
- Индексы созданы для часто запрашиваемых полей
- Используются select_related и prefetch_related для оптимизации запросов

## Тестирование

Проект полностью покрыт автоматическими тестами, включая:
- Модульные тесты для моделей
- Тесты сериализаторов
- Тесты представлений (views)
- Тесты API

### Запуск тестов

#### С использованием Docker:

```bash
# Запуск всех тестов
docker-compose -f docker-compose.test.yml up --build

# После завершения, отчет о покрытии будет доступен в директории htmlcov/
```

#### Локальный запуск:

```bash
# Установка зависимостей для тестирования
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск тестов с отчетом о покрытии
pytest --cov=departments

# Запуск тестов для конкретного модуля
pytest departments/tests/test_models.py

# Или можно использовать скрипт
./run_tests.sh
./run_tests.sh models  # только тесты моделей
./run_tests.sh api     # только тесты API
```

### Структура тестов

- `departments/tests/test_models.py` - тесты для моделей отделов и сотрудников
- `departments/tests/test_views.py` - тесты для Django представлений
- `departments/tests/test_api.py` - тесты для API эндпоинтов
- `departments/tests/factories.py` - фабрики для создания тестовых данных
- `departments/tests/conftest.py` - общие фикстуры для тестов

### Покрытие тестами

Текущее покрытие кода тестами составляет более 90% для основного функционала, включая:
- Модели: 100%
- Представления: 95%
- API эндпоинты: 95%
