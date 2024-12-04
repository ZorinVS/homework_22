from django.core.cache import cache
from django.http import Http404

from catalog.models import Product, Contact
from users.models import User

CATEGORIES_DICT = {
    "mailing-lists": "Рассылки",
    "telegram-bots": "Телеграм боты",
    "useful-utilities": "Полезные утилиты",
    "web-applications": "Веб-приложения",
    "microservices": "Микросервисы",
}


def get_products_list_from_cache(filter_by, value, products_key=None):
    """
    Получение списка продуктов из кеша

    :param filter_by: Поле, по которому выбираются продукты. Используемые значения:
        – `publication`: фильтрация по статусу публикации
        – `category`: фильтрация по названию категории продукта
        – `owner`: фильтрация по владельцу продукта
    :param value: Значение для фильтрации, зависящее от выбранного `filter_by`:
        – `publication`: True/False
        – `category`: название категории
        – `owner`: объект пользователя
    :param products_key: Ключ кеша. Если не указан при фильтрации по владельцу, ключ генерится из email пользователя
    """

    # Установка ключа кеша при фильтрации по владельцу
    if isinstance(value, User) and products_key is None:
        products_key = f"{value.email.split("@")[0]}_products"

    # Попытка получить данные из кеша
    queryset = cache.get(products_key)

    # Кеширование, если данных нет в кеше
    if not queryset:
        if filter_by == "publication":
            queryset = Product.objects.filter(is_published=value)
        elif filter_by == "category":
            queryset = Product.objects.filter(category__name=value)
        elif filter_by == "owner":
            queryset = Product.objects.filter(owner=value)
        if queryset:  # Избежание кеширования пустого QuerySet
            queryset = queryset.order_by("-created_at")
            cache.set(products_key, queryset, 60 * 15)  # 15 мин

    return queryset


def get_unpublished_products(queryset, user):
    """
    Получение списка неопубликованных продуктов на основе прав пользователя

    – Владелец видит только свои неопубликованные продукты
    – Модератор и администратор видят неопубликованные продукты всех пользователей

    :param queryset: QuerySet со всеми неопубликованными продуктами
    :param user: Объект авторизованного пользователя
    """

    if not user.has_perm("catalog.can_unpublish_product"):
        queryset = queryset.filter(owner=user)

    return queryset


def get_products_by_category(category_key):
    """ Получение списка продуктов в указанной категории """
    category_name = CATEGORIES_DICT.get(category_key)
    if not category_name:
        raise Http404("Category not found")
    queryset = get_products_list_from_cache(products_key=category_key, filter_by="category", value=category_name)
    return category_name, queryset


def set_context_data(context, **kwargs):
    """ Расширение контекста """
    for variable, value in kwargs.items():
        context[variable] = value
    return context


def get_contact_info(context):
    """ Получение свежей контактной информации """
    # Попытка получить данные из кеша
    contacts = cache.get("contacts_info")

    # Кеширование, если данных нет в кеше
    if not contacts:
        contacts = Contact.objects.order_by("-id")
        if contacts:  # Избежание кеширования пустого QuerySet
            cache.set("contacts_info", contacts, 60 * 60 * 12)  # 12 ч

    # Добавление свежей контактной информации, если имеется
    context["contact_info"] = contacts.first()

    return context
