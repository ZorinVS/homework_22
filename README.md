# Skystore

## Описание

Проект представляет собой интернет-магазин.

На текущем этапе проект включает:

- Настройку Django-проекта
- Создание и регистрацию приложения `catalog`
- Настройку маршрутизации для главной страницы и страницы с контактной информацией
- Подготовку HTML-шаблонов с использованием Bootstrap
- Реализацию базовых контроллеров для отображения домашней страницы и страницы контактов
- Подключение СУБД PostgreSQL для работы с данными 
- Создание моделей `Product`, `Category` и `Contact` в приложении каталога 
- Миграции для базы данных и их применение 
- Настройку административной панели, создание суперпользователя и заполнение контактной информации через админку
- Заполнение данных для моделей `Product` и `Category` через `shell -i ipython`
- Создание фикстур для моделей `Product`, `Category` и `Contact`

## Зависимости

- Python 3.12
- click 8.1.7
- decorator 5.1.1
- Django 5.1.2
- executing 2.1.0
- ipython 8.28.0
- packaging 24.1
- pathspec 0.12.1
- pexpect 4.9.0
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

## Запуск
1. В командной строке: `python3 manage.py runserver`
2. В браузере: http://127.0.0.1:8000/
