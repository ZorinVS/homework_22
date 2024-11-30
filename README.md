# Skystore

## Описание

Проект представляет собой интернет-магазин.

На текущем этапе проект включает:

- Настройку Django-проекта
- Создание и регистрацию приложений `catalog`, `blog`, `users`
- Настройку маршрутизации для главной страницы и страницы с контактной информацией
- Настройку маршрутизации для страниц Блога:
- Настройку маршрутизации для работы с пользователем
- Подготовку HTML-шаблонов с использованием Bootstrap
- Реализацию базовых контроллеров для отображения страниц
- Подключение СУБД PostgreSQL для работы с данными 
- Создание моделей `Product`, `Category` и `Contact` в приложении каталога 
- Создание модели `Article` в приложении блога 
- Создание моделей `User`, `UserManager` в приложении пользователи
- Миграции для базы данных и их применение 
- Настройку административной панели, создание суперпользователя и заполнение контактной информации через админку
- Заполнение данных для моделей `Product` и `Category` через `shell -i ipython`

## Зависимости

- Python 3.12
- asttokens 2.4.1
- click 8.1.7
- decorator 5.1.1
- Django 5.1.2
- django-phonenumber-field 8.0.0
- executing 2.1.0
- ipython 8.28.0
- packaging 24.1
- pathspec 0.12.1
- pexpect 4.9.0
- phonenumberslite 8.13.50
- pillow 11.0.0
- platformdirs 4.3.6
- prompt_toolkit 3.0.48
- psycopg2-binary 2.9.10
- ptyprocess 0.7.0
- pure_eval  2.3
- Pygments 2.18.0
- python-dotenv 1.0.1
- six 1.16.0
- sqlparse 0.5.1
- stack-data 0.6.3
- tabulate 0.9.0
- traitlets 5.14.3
- wcwidth 0.2.13



## Установка

1. Клонируйте репозиторий:
```bash
git clone git@github.com:ZorinVS/homework_22.git
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Подключение БД
1. Создайте БД
2. Создайте файл `.env` из файла `.env.sample`

## Применение миграций
```bash
python manage.py migrate
```

## Создание суперпользователя
- С помощью менеджера:
```bash
python3 manage.py createsuperuser
```
- С помощью кастомной команды:
```bash
python3 manage.py csu
```

## Наполнение данными
Тестовые данные для всего проекта:
```bash
python3 manage.py load_test_data
```

## Запуск
1. В командной строке: `python3 manage.py runserver`
2. В браузере: http://127.0.0.1:8000/
